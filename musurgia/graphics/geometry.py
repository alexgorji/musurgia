from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

Scalar = Decimal | int


@dataclass(frozen=True)
class Size:
    width: Scalar
    height: Scalar


@dataclass(frozen=True)
class Margins:
    top: Scalar = Decimal(0)
    right: Scalar = Decimal(0)
    bottom: Scalar = Decimal(0)
    left: Scalar = Decimal(0)

    def to_values(self) -> tuple[Scalar, Scalar, Scalar, Scalar]:
        return (self.top, self.right, self.bottom, self.left)


@dataclass(frozen=True)
class Paddings:
    top: Scalar = Decimal(0)
    right: Scalar = Decimal(0)
    bottom: Scalar = Decimal(0)
    left: Scalar = Decimal(0)

    def to_values(self) -> tuple[Scalar, Scalar, Scalar, Scalar]:
        return (self.top, self.right, self.bottom, self.left)


@dataclass(frozen=True)
class Position:
    x: Scalar
    y: Scalar

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)

    @staticmethod
    def from_values(x: Scalar, y: Scalar) -> "Position":
        return Position(x, y)

    def to_values(self) -> tuple[Scalar, Scalar]:
        return (self.x, self.y)


@dataclass(frozen=True)
class Coordinates:
    tl: Position
    tr: Position
    br: Position
    bl: Position


class LineOrientation(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
