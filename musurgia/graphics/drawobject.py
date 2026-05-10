from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
import math
from typing import Any
import cairo

from musurgia.graphics.defaults import DEFAULT_COLOR, DEFAULT_THICKNESS
from musurgia.graphics.geometry import Coordinates, Paddings, Position, Scalar, Size
from musurgia.graphics.geometry import LineOrientation
from musurgia.graphics.util import convert_to_scalar


def create_measure_context() -> cairo.Context:  # type: ignore[type-arg]
    # tiny dummy surface is enough for measurement
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1)
    return cairo.Context(surface)


@dataclass
class ColorMixin:
    color: str = DEFAULT_COLOR


@dataclass
class ThicknessMixin:
    thickness: Scalar = DEFAULT_THICKNESS


@dataclass
class LineOptions(ColorMixin, ThicknessMixin):
    stroke_dasharray: list[Scalar] | None = None


@dataclass
class TextOptions(ColorMixin):
    font_family: str = "DejaVu Sans"
    font_size: Scalar = 12


@dataclass
class RectangleOptions(ColorMixin, ThicknessMixin):
    stroke_dasharray: list[Scalar] | None = None
    fillcolor: str | None = None


@dataclass
class DrawObjectBoxOptions(RectangleOptions):
    color: str = "green"
    thickness: Scalar = Decimal("0.5")
    fillcolor: None = None


class DrawObjectBox:
    def __init__(
        self,
        *,
        draw_object: "DrawObject",
        show: bool = False,
        options: DrawObjectBoxOptions | None = None,
    ):
        self._draw_object = draw_object
        self._rectangle = None
        self.options = options or DrawObjectBoxOptions()
        self.show = show

    @property
    def draw_object(self) -> "DrawObject":
        return self._draw_object

    @property
    def size(self) -> Size:
        do = self.draw_object
        coor = self.draw_object.get_bounding_box_coordinates()
        width, height = coor.tr.x - coor.tl.x, coor.bl.y - coor.tl.y

        padding = getattr(do, "padding", None)
        if padding is not None:
            width += padding.left + padding.right
            height += padding.top + padding.bottom

        return Size(width, height)

    def get_rectangle(self) -> "Rectangle":
        rectangle = Rectangle(size=self.size, options=self.options)
        return rectangle


# -----------------------------
# Core drawable abstraction
# -----------------------------


class DrawObject(ABC):
    def __init__(self) -> None:
        self._box = DrawObjectBox(draw_object=self)
        self.show = True

    @property
    @abstractmethod
    def size(self) -> Size:
        raise NotImplementedError

    @property
    def box(self) -> DrawObjectBox:
        return self._box

    @abstractmethod
    def get_bounding_box_coordinates(self) -> Coordinates:
        pass


# -----------------------------
# Draw objects
# -----------------------------


class Text(DrawObject):
    def __init__(
        self,
        *,
        text: str,
        padding: Paddings = Paddings(),
        options: TextOptions | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.text = text
        self.padding = padding
        self.options: TextOptions = options or TextOptions()

    @staticmethod
    def convert_font_size_to_mm(font_size: Scalar) -> Decimal:
        return font_size * Decimal("25.4") / Decimal("72")

    @property
    def size(self) -> Size:
        ext = self.get_text_extents()
        return Size(width=Decimal(str(ext.width)), height=Decimal(str(ext.height)))

    def get_text_extents(self) -> cairo.TextExtents:
        ctx = create_measure_context()
        ctx.save()
        ctx.select_font_face(self.options.font_family)
        ctx.set_font_size(float(self.convert_font_size_to_mm(self.options.font_size)))
        ext = ctx.text_extents(self.text)
        ctx.restore()
        return ext

    def get_bounding_box_coordinates(self) -> Coordinates:
        return Coordinates(
            Position(0, 0),
            Position(self.size.width, 0),
            Position(self.size.width, self.size.height),
            Position(0, self.size.height),
        )


class Line(DrawObject):
    def __init__(
        self,
        *,
        start: Position = Position(0, 0),
        end: Position,
        options: LineOptions | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.start = start
        self.end = end
        self.options = options or LineOptions()

    def get_bounding_box_coordinates(self) -> Coordinates:
        x1, y1 = self.start.x, self.start.y

        x2, y2 = self.end.x, self.end.y

        # vector
        dx = x2 - x1
        dy = y2 - y1
        length = Decimal(str(math.hypot(dx, dy)))

        if length == 0:
            raise ValueError()

        # normalized direction vector (length 1)
        ux = dx / length
        uy = dy / length

        # unit normal vector(orthogonal)
        nx = -uy
        ny = ux

        half_th = convert_to_scalar(self.options.thickness / 2)

        # corners of the rotated rectangle"
        p1 = (x1 + nx * half_th, y1 + ny * half_th)
        p2 = (x1 - nx * half_th, y1 - ny * half_th)
        p3 = (x2 + nx * half_th, y2 + ny * half_th)
        p4 = (x2 - nx * half_th, y2 - ny * half_th)

        xs = [p1[0], p2[0], p3[0], p4[0]]
        ys = [p1[1], p2[1], p3[1], p4[1]]

        xmin = min(xs)
        xmax = max(xs)
        ymin = min(ys)
        ymax = max(ys)

        return Coordinates(
            Position(xmin, ymin),
            Position(xmax, ymin),
            Position(xmax, ymax),
            Position(xmin, ymax),
        )

    @property
    def size(self) -> Size:
        coor = self.get_bounding_box_coordinates()
        return Size(coor.tr.x - coor.tl.x, coor.bl.y - coor.tl.y)

    def get_length(self) -> Decimal:
        return Decimal(
            str(math.hypot(self.end.x - self.start.x, self.end.y - self.start.y))
        )


class StraightLine(DrawObject):
    def __init__(
        self,
        *,
        type: LineOrientation,
        length: Scalar,
        options: LineOptions | None = None,
    ) -> None:
        super().__init__()
        self.type = type
        self.length = length
        self.options = options or LineOptions()

    def get_bounding_box_coordinates(self) -> Coordinates:
        if self.type == LineOrientation.HORIZONTAL:
            xmin = convert_to_scalar(0)
            xmax = self.length
            ymin = -convert_to_scalar(self.options.thickness / 2)
            ymax = convert_to_scalar(self.options.thickness / 2)

        else:
            xmin = -convert_to_scalar(self.options.thickness / 2)
            xmax = convert_to_scalar(self.options.thickness / 2)
            ymin = convert_to_scalar(0)
            ymax = self.length

        return Coordinates(
            Position(xmin, ymin),
            Position(xmax, ymin),
            Position(xmax, ymax),
            Position(xmin, ymax),
        )

    @property
    def size(self) -> Size:
        coor = self.get_bounding_box_coordinates()
        return Size(coor.tr.x - coor.tl.x, coor.bl.y - coor.tl.y)


class Rectangle(DrawObject):
    def __init__(
        self,
        *,
        size: Size,
        padding: Paddings | None = None,
        options: RectangleOptions | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._size = size
        self.padding = padding or Paddings(0, 0, 0, 0)
        self.options = options or RectangleOptions()

    @property
    def size(self) -> Size:
        return self._size

    def get_bounding_box_coordinates(self) -> Coordinates:
        return Coordinates(
            Position(0, 0),
            Position(self.size.width, 0),
            Position(self.size.width, self.size.height),
            Position(0, self.size.height),
        )
