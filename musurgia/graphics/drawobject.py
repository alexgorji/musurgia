from dataclasses import dataclass, field
from typing import TypedDict, cast


class Position(TypedDict):
    x: int
    y: int


class Size(TypedDict):
    width: float
    height: float


@dataclass(frozen=True, kw_only=True)
class DrawObject:
    pass


class DrawObjectBox:
    def __init__(self):
        self._draw_objects: list[DrawObject] = []

    def add_draw_object(self, draw_object: DrawObject) -> "DrawObjectBox":
        self._draw_objects.append(draw_object)
        return self

    @property
    def size(self) -> Size:
        return {"width": self._get_width(), "height": self._get_height()}

    def _get_width(self) -> float:
        w = 0
        for draw_object in self._draw_objects:
            if isinstance(draw_object, HorizontalLineDrawObject):
                line_x2 = draw_object.start["x"] + draw_object.length
            elif isinstance(draw_object, VerticalLineDrawObject):
                line_x2 = draw_object.start["x"] + draw_object.stroke_width
            else:
                raise NotImplementedError

            if line_x2 > w:
                w = line_x2

        return w

    def _get_height(self) -> float:
        h = 0
        for draw_object in self._draw_objects:
            if isinstance(draw_object, VerticalLineDrawObject):
                line_y2 = draw_object.start["y"] + draw_object.length
            elif isinstance(draw_object, HorizontalLineDrawObject):
                line_y2 = draw_object.start["y"] + draw_object.stroke_width
            else:
                raise NotImplementedError

            if line_y2 > h:
                h = line_y2

        return h


@dataclass(frozen=True, kw_only=True)
class TextDrawObject(DrawObject):
    start: Position = cast(Position, field(default_factory=lambda: {"x": 0, "y": 0}))
    text: str
    font_family: str = "Helvetica"
    font_size: int = 12
    color: str = "black"


@dataclass(frozen=True, kw_only=True)
class LineDrawObject(DrawObject):
    end: Position
    start: Position = cast(Position, field(default_factory=lambda: {"x": 0, "y": 0}))
    color: str = "black"
    stroke_width: float = 0.1


@dataclass(frozen=True, kw_only=True)
class VerticalLineDrawObject(LineDrawObject):
    length: int
    end: Position = field(init=False)

    def __post_init__(self):
        object.__setattr__(
            self, "end", {"x": self.start["x"], "y": self.start["y"] + self.length}
        )


@dataclass(frozen=True, kw_only=True)
class HorizontalLineDrawObject(LineDrawObject):
    length: int
    end: Position = field(init=False)

    def __post_init__(self):
        object.__setattr__(
            self,
            "end",
            {"x": self.start["x"] + self.length, "y": self.start["y"]},
        )
