from musurgia.graphics.drawobject import (
    Container,
    HorizontalLineDrawObject,
    Position,
    VerticalLineDrawObject,
)

from enum import Enum
from dataclasses import dataclass, field, asdict, is_dataclass
from typing import Any, Mapping


class MarkerType(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


@dataclass
class MarkerOptions:
    length: float = 6.0
    thickness: float = 0.1
    color: str = "black"


@dataclass
class StraightLineOptions:
    thickness: float = 0.1
    color: str = "black"


@dataclass
class SegmentedLineOptions:
    start_marker: MarkerOptions = field(default_factory=MarkerOptions)
    end_marker: MarkerOptions = field(default_factory=MarkerOptions)
    straight_line: StraightLineOptions = field(default_factory=StraightLineOptions)


def _apply_overrides(obj: Any, overrides: Mapping[str, Any]) -> None:
    # obj is a dataclass
    # overrides is a dict
    for key, value in overrides.items():
        if not hasattr(obj, key):
            raise ValueError(f"Invalid option: {key}")

        current = getattr(obj, key)

        if isinstance(value, Mapping):
            if not is_dataclass(current):
                raise ValueError(
                    f"Cannot apply nested overrides to non-dataclass field '{key}'"
                )
            _apply_overrides(current, value)
        else:
            setattr(obj, key, value)


class LabeledContainer(Container):
    def __init__(self):
        super().__init__()
        self._labels = []


class Marker(LabeledContainer):
    def __init__(
        self,
        type: MarkerType,
        options: Mapping[str, Any] | None = None,
    ):
        super().__init__()
        self._type = type
        self._options = MarkerOptions()
        if options:
            _apply_overrides(self._options, options)
        self._line: HorizontalLineDrawObject | VerticalLineDrawObject
        self._build()

    def _build(self):
        if self._type == MarkerType.HORIZONTAL:
            self._line = HorizontalLineDrawObject(**asdict(self._options))
        else:
            self._line = VerticalLineDrawObject(**asdict(self._options))

    def get_type(self) -> str:
        return self._type.value

    def get_length(self) -> float:
        return self._line.get_length()

    def get_thickness(self) -> float:
        return self._line.thickness

    def get_color(self) -> str:
        return self._line.color


class HorizontalSegmentedLine(Container):
    def __init__(
        self,
        length: float,
        options: Mapping[str, Any] | None = None,
    ):
        super().__init__()
        self._length = length
        self._options = SegmentedLineOptions()
        if options:
            _apply_overrides(self._options, options)

        self._straight_line: HorizontalLineDrawObject
        self._start_marker: Marker
        self._end_marker: Marker

        self._build()

    def _build(self) -> None:
        self._start_marker = Marker(
            MarkerType.VERTICAL, asdict(self._options.start_marker)
        )

        self._end_marker = Marker(MarkerType.VERTICAL, asdict(self._options.end_marker))

        self._straight_line = HorizontalLineDrawObject(
            length=self._length, **asdict(self._options.straight_line)
        )

        self.add_draw_object(Position(0, 0), self._start_marker)
        self.add_draw_object(Position(self._length, 0), self._end_marker)
        self.add_draw_object(
            Position(
                0,
                max(self._end_marker.get_length(), self._start_marker.get_length()) / 2,
            ),
            self._straight_line,
        )

    def get_markers(self) -> tuple[Marker, Marker]:
        return self._start_marker, self._end_marker

    def get_straight_line(self) -> HorizontalLineDrawObject:
        return self._straight_line
