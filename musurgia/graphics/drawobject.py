from dataclasses import dataclass, field
from typing import TypedDict, cast


class Position(TypedDict):
    x: int
    y: int


class AbsolutePosition(TypedDict):
    x: int
    y: int


class RelativePosition(TypedDict):
    relative_x: int
    relative_y: int


@dataclass(frozen=True, kw_only=True)
class DrawObject:
    pass


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
