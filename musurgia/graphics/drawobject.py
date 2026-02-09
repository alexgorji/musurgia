from abc import ABC, abstractmethod
from dataclasses import dataclass
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
        return Size(
            do.size.width + do.padding.right + do.padding.left,
            do.size.height + do.padding.top + do.padding.bottom,
        )

    def get_rectangle(self):
        if not self._rectangle:
            self._get_rectangle = RectangleDrawObject(size=self.size, color="green")
        return self._get_rectangle


# -----------------------------
# Core drawable abstraction
# -----------------------------


class DrawObject(ABC):
    def __init__(self) -> None:
        self._box = DrawObjectBox(self)
        self._measure_ctx: cairo.Context | None = None

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

    def _get_measure_ctx(self) -> cairo.Context:
        if self._measure_ctx is None:
            self._measure_ctx = create_measure_context()
        return self._measure_ctx

    @abstractmethod
    def _get_padding(self) -> Padding:
        pass


# -----------------------------
# Container
# -----------------------------


class Container(DrawObject):
    def __init__(self):
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
            x2 = position.x + draw_object.size.width
            if x2 > w:
                w = x2
        return w

    def _get_height(self):
        h = 0.0
        for position, draw_object in self._draw_objects:
            y2 = position.y + draw_object.size.height
            if y2 > h:
                h = y2
        return h


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
        ctx = self._get_measure_ctx()
        ctx.save()
        ctx.select_font_face(self.font_family)
        ctx.set_font_size(self.font_size)
        ext = ctx.text_extents(self.text)
        ctx.restore()
        return Size(width=ext.width, height=ext.height)

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

    def _build_path(self, ctx: cairo.Context) -> None:
        """
        Prepares the path in the Cairo context for this line.
        Does NOT stroke or fill.
        """
        ctx.new_path()
        ctx.set_line_width(self.thickness)
        ctx.move_to(self.start.x, self.start.y)
        ctx.line_to(self.end.x, self.end.y)

    def _get_padding(self):
        return Padding(
            top=self.start.y,
            right=self.right_padding,
            bottom=self.bottom_padding,
            left=self.start.x,
        )

    @property
    def size(self):
        ctx = self._get_measure_ctx()
        ctx.save()
        self._build_path(ctx)
        x1, y1, x2, y2 = ctx.path_extents()
        ctx.restore()
        return Size(width=x2 - x1, height=y2 - y1)


class VerticalLineDrawObject(LineDrawObject):
    def __init__(self, *, start: Position = Position(0, 0), length: float, **kwargs):
        end = Position(start.x, start.y + length)
        super().__init__(start=start, end=end, **kwargs)


class HorizontalLineDrawObject(LineDrawObject):
    def __init__(self, *, start: Position = Position(0, 0), length: float, **kwargs):
        end = Position(start.x + length, start.y)
        super().__init__(start=start, end=end, **kwargs)


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
