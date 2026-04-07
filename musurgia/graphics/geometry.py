from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Size:
    width: float
    height: float


@dataclass(frozen=True)
class Paddings:
    top: float | int = 0
    right: float | int = 0
    bottom: float | int = 0
    left: float | int = 0


@dataclass(frozen=True)
class Position:
    x: float
    y: float

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)

    @staticmethod
    def from_values(x: float, y: float) -> "Position":
        return Position(x, y)


@dataclass(frozen=True)
class Coordinates:
    tl: Position
    tr: Position
    br: Position
    bl: Position


@dataclass
class Margins:
    top: int
    right: int
    bottom: int
    left: int


class LineOrientation(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
