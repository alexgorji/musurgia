from abc import ABC, abstractmethod
from dataclasses import dataclass
import math
from typing import Any, List, Tuple
import cairo


def create_measure_context() -> cairo.Context:  # type: ignore[type-arg]
    # tiny dummy surface is enough for measurement
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1)
    return cairo.Context(surface)


# -----------------------------
# Value objects (dataclasses)
# -----------------------------


@dataclass(frozen=True)
class Position:
    x: float
    y: float

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    @staticmethod
    def from_values(x: float, y: float) -> "Position":
        return Position(x, y)


@dataclass(frozen=True)
class Size:
    width: float
    height: float


@dataclass(frozen=True)
class Padding:
    top: float
    right: float
    bottom: float
    left: float


@dataclass(frozen=True)
class Coordinates:
    tl: Position
    tr: Position
    br: Position
    bl: Position


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

        return Size(
            width + do.padding.right + do.padding.left,
            height + do.padding.top + do.padding.bottom,
        )

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

    @property
    def padding(self) -> Padding:
        return self._get_padding()

    @abstractmethod
    def _get_padding(self) -> Padding:
        pass

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


# -----------------------------
# Container
# -----------------------------


class Container(DrawObject):
    def __init__(self) -> None:
        super().__init__()
        self._draw_objects: List[Tuple[Position, DrawObject]] = []
        self._padding = Padding(0, 0, 0, 0)

    def _get_padding(self) -> "Padding":
        return self._padding

    def add_draw_object(
        self, position: Position, draw_object: DrawObject
    ) -> "Container":
        self._draw_objects.append((position, draw_object))
        return self

    def get_draw_objects(
        self, recursive: bool = False
    ) -> List[Tuple[Position, DrawObject]]:
        if recursive:
            return_value = []
            for p, o in self._draw_objects:
                if not isinstance(o, Container):
                    return_value.append((p, o))
                else:
                    return_value.extend(
                        [(p + pp, oo) for pp, oo in o.get_draw_objects(recursive=True)]
                    )
            return return_value

        return self._draw_objects

    @property
    def size(self) -> Size:
        coor = self.get_bounding_box_coordinates()
        return Size(coor.tr.x - coor.tl.x, coor.bl.y - coor.tl.y)

    def get_bounding_box_coordinates(self) -> Coordinates:
        tl, tr, br, bl = [
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 0.0],
        ]
        for p, d in self.get_draw_objects():
            coor = d.get_bounding_box_coordinates()
            if coor.tl.x + p.x < tl[0]:
                tl[0] = coor.tl.x + p.x
            if coor.tl.y + p.y < tl[1]:
                tl[1] = coor.tl.y + p.y
            if coor.tr.x + p.x > tr[0]:
                tr[0] = coor.tr.x + p.x
            if coor.tr.y + p.y < tr[1]:
                tr[1] = coor.tr.y + p.y
            if coor.br.x + p.x > br[0]:
                br[0] = coor.br.x + p.x
            if coor.br.y + p.y > br[1]:
                br[1] = coor.br.y + p.y
            if coor.bl.x + p.x < bl[0]:
                bl[0] = coor.bl.x + p.x
            if coor.bl.y + p.y > bl[1]:
                bl[1] = coor.bl.y + p.y

        return Coordinates(
            Position.from_values(*tl),
            Position.from_values(*tr),
            Position.from_values(*br),
            Position.from_values(*bl),
        )


# -----------------------------
# Draw objects
# -----------------------------
class TextDrawObject(ColorMixin, DrawObject):
    def __init__(
        self,
        *,
        text: str,
        start: Position = Position(0, 0),
        right_padding: int | float = 0,
        bottom_padding: int | float = 0,
        font_family: str = "Helvetica",
        font_size: int | float = 12,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._text = text
        self._start = start
        self._right_padding = right_padding
        self._bottom_padding = bottom_padding

        self._font_family = font_family
        self._font_size = font_size

    @staticmethod
    def convert_font_size_to_mm(font_size: int | float) -> float:
        return font_size * 25.4 / 72

    @property
    def text(self) -> str:
        return self._text

    @property
    def start(self) -> Position:
        return self._start

    @property
    def right_padding(self) -> int | float:
        return self._right_padding

    @property
    def bottom_padding(self) -> int | float:
        return self._bottom_padding

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

    def _get_padding(self) -> Padding:
        return Padding(
            top=self.start.y,
            right=self.right_padding,
            bottom=self.bottom_padding,
            left=self.start.x,
        )

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
        right_padding: int | float = 0,
        bottom_padding: int | float = 0,
        thickness: float = 0.1,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._start = start
        self._end = end
        self._right_padding = right_padding
        self._bottom_padding = bottom_padding
        self._thickness = thickness

    @property
    def start(self) -> Position:
        return self._start

    @property
    def end(self) -> Position:
        return self._end

    @property
    def right_padding(self) -> int | float:
        return self._right_padding

    @property
    def bottom_padding(self) -> int | float:
        return self._bottom_padding

    @property
    def thickness(self) -> float:
        return self._thickness

    def set_thickness(self, val: float) -> None:
        self._thickness = val

    def _get_padding(self) -> Padding:
        return Padding(
            top=min(self.start.y, self.end.y),
            right=self.right_padding,
            bottom=self.bottom_padding,
            left=min(self.start.x, self.end.x),
        )

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


class VerticalLineDrawObject(LineDrawObject):
    def __init__(
        self,
        *,
        start: Position = Position(0, 0),
        length: float,
        thickness: float = 0.1,
        right_padding: int | float = 0,
        bottom_padding: int | float = 0,
        **kwargs: Any,
    ) -> None:
        end = Position(start.x, start.y + length)
        super().__init__(
            start=start,
            end=end,
            thickness=thickness,
            right_padding=right_padding,
            bottom_padding=bottom_padding,
            **kwargs,
        )


class HorizontalLineDrawObject(LineDrawObject):
    def __init__(
        self,
        *,
        start: Position = Position(0, 0),
        length: float,
        thickness: float = 0.1,
        right_padding: int | float = 0,
        bottom_padding: int | float = 0,
        **kwargs: Any,
    ) -> None:
        end = Position(start.x + length, start.y)
        super().__init__(
            start=start,
            end=end,
            thickness=thickness,
            right_padding=right_padding,
            bottom_padding=bottom_padding,
            **kwargs,
        )


class RectangleDrawObject(ColorMixin, DrawObject):
    def __init__(
        self,
        *,
        size: Size,
        padding: Padding = Padding(0, 0, 0, 0),
        thickness: float = 0.1,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._size = size
        self._padding = padding
        self._thickness = thickness

    def _get_padding(self) -> Padding:
        return self._padding

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
