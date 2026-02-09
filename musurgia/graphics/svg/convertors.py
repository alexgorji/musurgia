from abc import ABC, abstractmethod
from typing import Dict, Generic, TypeVar
import svg
from musurgia.graphics.drawobject import (
    DrawObject,
    HorizontalLineDrawObject,
    LineDrawObject,
    Position,
    RectangleDrawObject,
    TextDrawObject,
    Container,
    VerticalLineDrawObject,
)

T = TypeVar("T", bound=DrawObject)


class DrawObjectConvertor(ABC, Generic[T]):
    def __init__(self, position: Position, draw_object: T):
        self.position = position
        self.draw_object = draw_object

    def convert_box(self):
        return RectangleDrawObjectToSVGConvertor(
            self.position, self.draw_object.box.get_rectangle()
        ).convert()

    @abstractmethod
    def convert(self) -> svg.Element:
        pass


class TextDrawObjectToSVGConvertor(DrawObjectConvertor[TextDrawObject]):
    def get_font_size_mm(self):
        return self.draw_object.font_size * 25.4 / 72

    def convert(self):
        return svg.Text(
            x=self.draw_object.start.x + self.position.x,
            y=self.draw_object.start.y + self.position.y,
            text=self.draw_object.text,
            font_size=self.get_font_size_mm(),
            font_family=self.draw_object.font_family,
            fill=self.draw_object.color,
        )


class LineDrawObjectToSVGConvertor(DrawObjectConvertor[LineDrawObject]):
    def convert(self):
        return svg.Line(
            x1=self.draw_object.start.x + self.position.x,
            y1=self.draw_object.start.y + self.position.y,
            x2=self.draw_object.end.x + self.position.x,
            y2=self.draw_object.end.y + self.position.y,
            stroke=self.draw_object.color,
            stroke_width=self.draw_object.thickness,
        )


class RectangleDrawObjectToSVGConvertor(DrawObjectConvertor[RectangleDrawObject]):
    def convert(self):
        return svg.Rect(
            x=self.position.x + self.draw_object.padding.left,
            y=self.position.y + self.draw_object.padding.top,
            width=self.draw_object.size.width,
            height=self.draw_object.size.height,
            stroke=self.draw_object.color,
            fill="transparent",
            stroke_width=self.draw_object.thickness,
        )


U = TypeVar("U", bound=DrawObject)


class SVGConverterRegistry:
    _registry: Dict[type[DrawObject], type[DrawObjectConvertor]] = {}

    @classmethod
    def register(cls, draw_type: type[U], converter_cls: type[DrawObjectConvertor[U]]):
        cls._registry[draw_type] = converter_cls

    @classmethod
    def convert(
        cls,
        position: Position,
        draw_object: DrawObject | Container,
    ) -> list[svg.Element]:
        if isinstance(draw_object, Container):
            elements: list[svg.Element] = []
            for pos, obj in draw_object.get_draw_objects():
                elements.extend(cls.convert(position + pos, obj))
            return elements

        try:
            converter_cls = cls._registry[type(draw_object)]
        except KeyError:
            raise TypeError(f"No SVG converter for {type(draw_object)}")

        converter = converter_cls(position, draw_object)
        converted = [converter.convert()]
        if draw_object.box.show:
            converted.append(converter.convert_box())
        return converted


SVGConverterRegistry.register(LineDrawObject, LineDrawObjectToSVGConvertor)
SVGConverterRegistry.register(HorizontalLineDrawObject, LineDrawObjectToSVGConvertor)
SVGConverterRegistry.register(VerticalLineDrawObject, LineDrawObjectToSVGConvertor)
SVGConverterRegistry.register(TextDrawObject, TextDrawObjectToSVGConvertor)
SVGConverterRegistry.register(RectangleDrawObject, RectangleDrawObjectToSVGConvertor)
