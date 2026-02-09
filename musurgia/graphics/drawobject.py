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
class DrawObjectBox:
    def __init__(self, draw_object: "DrawObject", show=False):
        self._draw_object = draw_object
        self.show = show

    @property
    def draw_object(self):
        return self._draw_object

    @property
    def size(self) -> Size:
        return self.draw_object.size


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

    def _get_measure_ctx(self) -> cairo.Context:
        if self._measure_ctx is None:
            self._measure_ctx = create_measure_context()
        return self._measure_ctx


# -----------------------------
# Container
# -----------------------------


class Container(DrawObject):
    def __init__(self):
        self._draw_objects: List[Tuple[Position, DrawObject]] = []

    def add_draw_object(
        self, position: Position, draw_object: DrawObject
    ) -> "Container":
        self._draw_objects.append((position, draw_object))
        return self

    def get_draw_objects(self):
        return self._draw_objects

    @property
    def size(self) -> Size:
        return Size(self._get_width(), self._get_height())

    def _get_width(self) -> float:
        w = 0.0
        for position, draw_object in self._draw_objects:
            x2 = position.x + draw_object.size.width
            if x2 > w:
                w = x2
        return w

    def _get_height(self) -> float:
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
        font_family: str = "Helvetica",
        font_size: int = 12,
        color: str = "black",
    ):
        super().__init__()
        self.start = start
        self.text = text
        self.font_family = font_family
        self.font_size = font_size
        self.color = color

    @property
    def size(self) -> Size:
        ctx = self._get_measure_ctx()
        ctx.save()
        ctx.select_font_face(self.font_family)
        ctx.set_font_size(self.font_size)
        ext = ctx.text_extents(self.text)
        ctx.restore()
        return Size(width=ext.width, height=ext.height)


class LineDrawObject(DrawObject):
    def __init__(
        self,
        *,
        start: Position = Position(0, 0),
        end: Position,
        color: str = "black",
        thickness: float = 2,
    ):
        super().__init__()
        self.start = start
        self.end = end
        self.color = color
        self.thickness = thickness


    def _build_path(self, ctx: cairo.Context) -> None:
        """
        Prepares the path in the Cairo context for this line.
        Does NOT stroke or fill.
        """
        ctx.new_path()
        ctx.set_line_width(self.thickness)
        ctx.move_to(self.start.x, self.start.y)
        ctx.line_to(self.end.x, self.end.y)

        # path_extents gives (x1, y1, x2, y2) of the bounding box
    @property
    def size(self) -> Size:
        ctx = self._get_measure_ctx()
        ctx.save()
        self._build_path(ctx)
        x1, y1, x2, y2 = ctx.path_extents()
        ctx.restore()
        return Size(width=x2 - x1, height=y2 - y1)


class VerticalLineDrawObject(LineDrawObject):
    def __init__(
        self,
        *,
        start: Position = Position(0, 0),
        length: float,
        color: str = "black",
        thickness: float = 2,
    ):
        end = Position(start.x, start.y + length)
        super().__init__(
            start=start,
            end=end,
            color=color,
            thickness=thickness,
        )


class HorizontalLineDrawObject(LineDrawObject):
    def __init__(
        self,
        *,
        start: Position = Position(0, 0),
        length: float,
        color: str = "black",
        thickness: float = 2,
    ):
        end = Position(start.x + length, start.y)
        super().__init__(
            start=start,
            end=end,
            color=color,
            thickness=thickness,
        )
