from abc import ABC, abstractmethod
from dataclasses import dataclass
import math
from typing import List, Tuple
import cairo


def create_measure_context() -> cairo.Context:
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

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    @staticmethod
    def from_values(values: Tuple[float, float]):
        return Position(values[0], values[1])


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
    def __init__(self, draw_object: "DrawObject", show=False):
        self._draw_object = draw_object
        self._rectangle = None
        self.show = show

    @property
    def draw_object(self):
        return self._draw_object

    @property
    def size(self):
        do = self.draw_object
        if coor := self.draw_object.get_bounding_box_coordinates():
            width, height = coor.tr.x - coor.tl.x, coor.bl.y - coor.tl.y
        else:
            width, height = do.size.width, do.size.height
        return Size(
            width + do.padding.right + do.padding.left,
            height + do.padding.top + do.padding.bottom,
        )

    def get_rectangle(self):
        rectangle = RectangleDrawObject(size=self.size, color="green")
        return rectangle


# -----------------------------
# Core drawable abstraction
# -----------------------------


class DrawObject(ABC):
    def __init__(self) -> None:
        self._box = DrawObjectBox(self)

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

    def get_bounding_box_coordinates(self) -> Coordinates | None:
        return None


# -----------------------------
# Container
# -----------------------------


class Container(DrawObject):
    def __init__(self):
        super().__init__()
        self._draw_objects: List[Tuple[Position, DrawObject]] = []
        self._padding = Padding(0, 0, 0, 0)

    def _get_padding(self):
        return self._padding

    def add_draw_object(
        self, position: Position, draw_object: DrawObject
    ) -> "Container":
        self._draw_objects.append((position, draw_object))
        return self

    def get_draw_objects(self):
        return self._draw_objects

    @property
    def size(self):
        return Size(self._get_width(), self._get_height())

    def _get_width(self):
        w = 0.0
        for position, draw_object in self._draw_objects:
            x2 = position.x + draw_object.box.size.width
            if x2 > w:
                w = x2
        return w

    def _get_height(self):
        h = 0.0
        for position, draw_object in self._draw_objects:
            y2 = position.y + draw_object.box.size.height
            if y2 > h:
                h = y2
        return h

    def get_bounding_box_coordinates(self):
        tl, tr, br, bl = [
            [0, 0],
            [self.size.width, 0],
            [self.size.width, self.size.height],
            [0, self.size.height],
        ]
        for _, do in self.get_draw_objects():
            if coor := do.get_bounding_box_coordinates():
                if coor.tl.x < tl[0]:
                    tl[0] = coor.tl.x
                if coor.tl.y < tl[1]:
                    tl[1] = coor.tl.y
                if coor.tr.x > tr[0]:
                    tr[0] = coor.tr.x
                if coor.tr.y < tr[1]:
                    tr[1] = coor.tr.y
                if coor.br.x > br[0]:
                    br[0] = coor.br.x
                if coor.br.y > br[1]:
                    br[1] = coor.br.y
                if coor.bl.x < bl[0]:
                    bl[0] = coor.bl.x
                if coor.bl.y > bl[1]:
                    bl[1] = coor.bl.y

        return Coordinates(
            Position.from_values(tuple(tl)),
            Position.from_values(tuple(tr)),
            Position.from_values(tuple(br)),
            Position.from_values(tuple(bl)),
        )


# -----------------------------
# Draw objects
# -----------------------------


class TextDrawObject(DrawObject):
    def __init__(
        self,
        *,
        text: str,
        start: Position = Position(0, 0),
        right_padding=0,
        bottom_padding=0,
        font_family: str = "Helvetica",
        font_size: int = 12,
        color: str = "black",
    ):
        super().__init__()
        self._text = text
        self._start = start
        self._right_padding = right_padding
        self._bottom_padding = bottom_padding

        self._font_family = font_family
        self._font_size = font_size
        self._color = color

    @staticmethod
    def convert_font_size_to_mm(font_size):
        return font_size * 25.4 / 72

    @property
    def text(self):
        return self._text

    @property
    def start(self):
        return self._start

    @property
    def right_padding(self):
        return self._right_padding

    @property
    def bottom_padding(self):
        return self._bottom_padding

    @property
    def font_family(self):
        return self._font_family

    @property
    def font_size(self):
        return self._font_size

    @property
    def color(self):
        return self._color

    def set_color(self, val):
        self._color = val

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

    def _get_padding(self):
        return Padding(
            top=self.start.y,
            right=self.right_padding,
            bottom=self.bottom_padding,
            left=self.start.x,
        )


class LineDrawObject(DrawObject):
    def __init__(
        self,
        *,
        start: Position = Position(0, 0),
        end: Position,
        right_padding=0,
        bottom_padding=0,
        color: str = "black",
        thickness: float = 0.1,
    ):
        super().__init__()
        self._start = start
        self._end = end
        self._right_padding = right_padding
        self._bottom_padding = bottom_padding
        self._color = color
        self._thickness = thickness

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def right_padding(self):
        return self._right_padding

    @property
    def bottom_padding(self):
        return self._bottom_padding

    @property
    def color(self):
        return self._color

    @property
    def thickness(self):
        return self._thickness

    def set_color(self, val):
        self._color = val

    def set_thickness(self, val):
        self._thickness = val

    def _get_padding(self):
        return Padding(
            top=self.start.y,
            right=self.right_padding,
            bottom=self.bottom_padding,
            left=self.start.x,
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
    def size(self):
        coor = self.get_bounding_box_coordinates()
        return Size(coor.tr.x - coor.tl.x, coor.bl.y - coor.tl.y)


class VerticalLineDrawObject(LineDrawObject):
    def __init__(
        self,
        *,
        start: Position = Position(0, 0),
        length: float,
        color: str = "black",
        thickness: float = 0.1,
        right_padding=0,
        bottom_padding=0,
    ):
        end = Position(start.x, start.y + length)
        super().__init__(
            start=start,
            end=end,
            color=color,
            thickness=thickness,
            right_padding=right_padding,
            bottom_padding=bottom_padding,
        )


class HorizontalLineDrawObject(LineDrawObject):
    def __init__(
        self,
        *,
        start: Position = Position(0, 0),
        length: float,
        color: str = "black",
        thickness: float = 0.1,
        right_padding=0,
        bottom_padding=0,
    ):
        end = Position(start.x + length, start.y)
        super().__init__(
            start=start,
            end=end,
            color=color,
            thickness=thickness,
            right_padding=right_padding,
            bottom_padding=bottom_padding,
        )


class RectangleDrawObject(DrawObject):
    def __init__(
        self,
        *,
        size: Size,
        padding=Padding(0, 0, 0, 0),
        color: str = "black",
        thickness: float = 0.1,
    ):
        super().__init__()
        self._size = size
        self._padding = padding
        self._color = color
        self._thickness = thickness

    def _get_padding(self):
        return self._padding

    @property
    def size(self):
        return self._size

    @property
    def color(self):
        return self._color

    @property
    def thickness(self):
        return self._thickness

    def set_color(self, val):
        self._color = val

    def set_thickness(self, val):
        self._thickness = val
