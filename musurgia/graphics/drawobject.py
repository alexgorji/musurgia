from dataclasses import dataclass, field
from typing import TypedDict


class AbsolutePosition(TypedDict):
    x: int
    y: int


class RelativePosition(TypedDict):
    relative_x: int
    relative_y: int


@dataclass(kw_only=True)
class DrawObjectLayout:
    relative_x: int = 0
    relative_y: int = 0

    def get_relative_position(self) -> RelativePosition:
        return {"relative_x": self.relative_x, "relative_y": self.relative_y}

    def get_absolute_position(self) -> AbsolutePosition:
        return {"x": self.relative_x, "y": self.relative_y}


@dataclass(kw_only=True)
class DrawObject:
    layout: DrawObjectLayout = field(default_factory=DrawObjectLayout)


@dataclass
class TextDrawObject(DrawObject):
    text: str
    font_family: str = "Helvetica"
    font_size: int = 12
    color: str = "black"
