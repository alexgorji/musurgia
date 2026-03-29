from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, TypeVar
import svg
from musurgia.graphics.drawobject import (
    DrawObject,
    StraightLineDrawObject,
    LineDrawObject,
    Position,
    RectangleDrawObject,
    TextDrawObject,
    Container,
)

T = TypeVar("T", bound=DrawObject)


class DrawObjectConvertor(ABC, Generic[T]):
    def __init__(self, position: Position, draw_object: T):
        self.position = position
        self.draw_object = draw_object

    def _convert_box(self) -> list[svg.Element]:
        position = self.position
        position += self.draw_object.get_bounding_box_coordinates().tl
        return RectangleDrawObjectToSVGConvertor(
            position,
            self.draw_object.box.get_rectangle(),
        ).convert()

    @abstractmethod
    def _convert(self) -> list[svg.Element]:
        pass

    def convert(self) -> list[svg.Element]:
        converted = []
        if self.draw_object.show:
            converted += self._convert()
        if self.draw_object.box.show:
            converted += self._convert_box()
        return converted


class TextDrawObjectToSVGConvertor(DrawObjectConvertor[TextDrawObject]):

    def _convert(self) -> list[svg.Element]:
        ext = self.draw_object.get_text_extents()
        return [
            svg.Text(
                x=self.draw_object.padding.left + self.position.x - ext.x_bearing,
                y=self.draw_object.padding.top + self.position.y - ext.y_bearing,
                text=self.draw_object.text,
                font_size=TextDrawObject.convert_font_size_to_mm(
                    self.draw_object.font_size
                ),
                font_family=self.draw_object.font_family,
                fill=self.draw_object.color,
            )
        ]


class LineDrawObjectToSVGConvertor(DrawObjectConvertor[LineDrawObject]):
    def _convert(self) -> list[svg.Element]:
        return [
            svg.Line(
                x1=self.draw_object.start.x + self.position.x,
                y1=self.draw_object.start.y + self.position.y,
                x2=self.draw_object.end.x + self.position.x,
                y2=self.draw_object.end.y + self.position.y,
                stroke=self.draw_object.color,
                stroke_width=self.draw_object.thickness,
            )
        ]


class RectangleDrawObjectToSVGConvertor(DrawObjectConvertor[RectangleDrawObject]):
    def _convert(self) -> list[svg.Element]:
        th = self.draw_object.thickness
        return [
            svg.Rect(
                x=self.position.x + self.draw_object.padding.left + th / 2,
                y=self.position.y + self.draw_object.padding.top + th / 2,
                width=self.draw_object.size.width - th,
                height=self.draw_object.size.height - th,
                stroke=self.draw_object.color,
                fill="transparent",
                stroke_width=self.draw_object.thickness,
            )
        ]


class ContainerToSVGConvertor(DrawObjectConvertor[Container]):
    def _convert(self) -> list[svg.Element]:
        elements: list[svg.Element] = []
        for pos, child in self.draw_object.get_positioned_draw_objects():
            elements.extend(SVGConverterRegistry.convert(self.position + pos, child))
        return elements


U = TypeVar("U", bound=DrawObject)


class SVGConverterRegistry:
    _registry: Dict[type[DrawObject], type[DrawObjectConvertor[Any]]] = {}

    @classmethod
    def register(
        cls, draw_type: type[U], converter_cls: type[DrawObjectConvertor[U]]
    ) -> None:
        cls._registry[draw_type] = converter_cls

    @classmethod
    def convert(cls, position: Position, draw_object: DrawObject) -> list[svg.Element]:
        try:
            converter_cls = cls._registry[type(draw_object)]
        except KeyError:
            if isinstance(draw_object, Container):
                converter_cls = cls._registry[Container]
            else:
                raise TypeError(f"No SVG converter for {type(draw_object)}")

        converter = converter_cls(position, draw_object)
        converted = converter.convert()

        return converted


SVGConverterRegistry.register(LineDrawObject, LineDrawObjectToSVGConvertor)
SVGConverterRegistry.register(StraightLineDrawObject, LineDrawObjectToSVGConvertor)
SVGConverterRegistry.register(TextDrawObject, TextDrawObjectToSVGConvertor)
SVGConverterRegistry.register(RectangleDrawObject, RectangleDrawObjectToSVGConvertor)
SVGConverterRegistry.register(Container, ContainerToSVGConvertor)
