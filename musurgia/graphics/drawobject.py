from abc import ABC, abstractmethod
import math
from typing import Any
import cairo

from musurgia.graphics.geometry import Coordinates, Paddings, Position, Size
from musurgia.graphics.geometry import LineOrientation


def create_measure_context() -> cairo.Context:  # type: ignore[type-arg]
    # tiny dummy surface is enough for measurement
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1)
    return cairo.Context(surface)


# -----------------------------
# Value objects (dataclasses)
# -----------------------------


class DrawObjectBox:
    def __init__(self, *, draw_object: "DrawObject", show: bool = False):
        self._draw_object = draw_object
        self._rectangle = None
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

    def get_rectangle(self) -> "RectangleDrawObject":
        rectangle = RectangleDrawObject(size=self.size, color="green")
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


class ColorMixin:
    def __init__(self, *, color: str = "black", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._color = color

    @property
    def color(self) -> str:
        return self._color

    def set_color(self, val: str) -> None:
        self._color = val

    def get_color(self) -> str:
        return self._color


# -----------------------------
# Draw objects
# -----------------------------
class TextDrawObject(ColorMixin, DrawObject):
    def __init__(
        self,
        *,
        text: str,
        padding: Paddings = Paddings(),
        font_family: str = "DejaVu Sans",
        font_size: int | float = 12,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._text = text
        self.padding = padding

        self._font_family = font_family
        self._font_size = font_size

    @staticmethod
    def convert_font_size_to_mm(font_size: int | float) -> float:
        return font_size * 25.4 / 72

    @property
    def text(self) -> str:
        return self._text

    @property
    def font_family(self) -> str:
        return self._font_family

    @property
    def font_size(self) -> int | float:
        return self._font_size

    @property
    def size(self) -> Size:
        ext = self.get_text_extents()
        return Size(width=ext.width, height=ext.height)

    def get_text_extents(self) -> cairo.TextExtents:
        ctx = create_measure_context()
        ctx.save()
        ctx.select_font_face(self.font_family)
        ctx.set_font_size(self.convert_font_size_to_mm(self.font_size))
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


class LineDrawObject(ColorMixin, DrawObject):
    def __init__(
        self,
        *,
        start: Position = Position(0, 0),
        end: Position,
        thickness: float = 0.1,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._start = start
        self._end = end
        self._thickness = thickness

    @property
    def start(self) -> Position:
        return self._start

    @property
    def end(self) -> Position:
        return self._end

    @property
    def thickness(self) -> float:
        return self._thickness

    def set_thickness(self, val: float) -> None:
        self._thickness = val

    def get_bounding_box_coordinates(self) -> Coordinates:
        x1, y1 = self.start.x, self.start.y

        x2, y2 = self.end.x, self.end.y

        # vector
        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)

        if length == 0:
            raise ValueError()

        # normalized direction vector (length 1)
        ux = dx / length
        uy = dy / length

        # unit normal vector(orthogonal)
        nx = -uy
        ny = ux

        half_th = self.thickness / 2

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

    def get_length(self) -> float:
        return math.hypot(self.end.x - self.start.x, self.end.y - self.start.y)


class StraightLineDrawObject(LineDrawObject):
    def __init__(
        self,
        *,
        type: LineOrientation,
        length: float,
        start: Position = Position(0, 0),
        thickness: float = 0.1,
        **kwargs: Any,
    ) -> None:
        self.type = type
        if type.value == "horizontal":
            end = Position(start.x + length, start.y)
        else:
            end = Position(start.x, start.y + length)
        super().__init__(
            start=start,
            end=end,
            thickness=thickness,
            **kwargs,
        )
        self.type = type


class RectangleDrawObject(ColorMixin, DrawObject):
    def __init__(
        self,
        *,
        size: Size,
        padding: Paddings = Paddings(0, 0, 0, 0),
        thickness: float = 0.1,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._size = size
        self.padding = padding
        self._thickness = thickness

    @property
    def size(self) -> Size:
        return self._size

    @property
    def thickness(self) -> float:
        return self._thickness

    def set_thickness(self, val: float) -> None:
        self._thickness = val

    def get_bounding_box_coordinates(self) -> Coordinates:
        return Coordinates(
            Position(0, 0),
            Position(self.size.width, 0),
            Position(self.size.width, self.size.height),
            Position(0, self.size.height),
        )
