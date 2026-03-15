from musurgia.graphics.drawobject import (
    Container,
    HorizontalLineDrawObject,
    Position,
    VerticalLineDrawObject,
)

from enum import Enum
from dataclasses import dataclass, field, asdict, fields
from typing import Any, Mapping

from musurgia.graphics.util import overrides_data_class_options


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
class LineSegmentOptions:
    start_marker: MarkerOptions = field(default_factory=MarkerOptions)
    end_marker: MarkerOptions = field(default_factory=MarkerOptions)
    straight_line: StraightLineOptions = field(default_factory=StraightLineOptions)


class Marker(Container):
    def __init__(
        self,
        *,
        type: MarkerType,
        options: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__()
        self._type = type
        self._options = MarkerOptions()
        if options:
            overrides_data_class_options(self._options, options)
        self._line: HorizontalLineDrawObject | VerticalLineDrawObject
        self._build()

    def _build(self) -> None:
        if self._type == MarkerType.HORIZONTAL:
            self._line = HorizontalLineDrawObject(**asdict(self._options))
        else:
            self._line = VerticalLineDrawObject(**asdict(self._options))
        self.add_draw_object(Position(0, 0), self._line)

    def get_type(self) -> str:
        return self._type.value

    def get_length(self) -> float:
        return self._line.get_length()

    def get_thickness(self) -> float:
        return self._line.thickness

    def get_color(self) -> str:
        return self._line.color


class HorizontalLineSegment(Container):
    def __init__(
        self,
        *,
        length: float,
        color: str | None = None,
        thickness: float | None = None,
        options: Mapping[str, Any] | None = None,
    ):
        super().__init__()
        self._length = length
        self._options = LineSegmentOptions()
        if color:
            for field in fields(self._options):
                component = getattr(self._options, field.name)
                if hasattr(component, "color"):
                    setattr(component, "color", color)
        if thickness:
            for field in fields(self._options):
                component = getattr(self._options, field.name)
                if hasattr(component, "thickness"):
                    setattr(component, "thickness", thickness)

        if options:
            overrides_data_class_options(self._options, options)

        self._straight_line: HorizontalLineDrawObject
        self._start_marker: Marker
        self._end_marker: Marker

        self._build()

    def _build(self) -> None:
        self._start_marker = Marker(
            type=MarkerType.VERTICAL, options=asdict(self._options.start_marker)
        )

        self._end_marker = Marker(
            type=MarkerType.VERTICAL, options=asdict(self._options.end_marker)
        )

        self._straight_line = HorizontalLineDrawObject(
            length=self._length, **asdict(self._options.straight_line)
        )

        start_marker_y_position = (
            0
            if self._start_marker.get_length() >= self._end_marker.get_length()
            else (self._end_marker.get_length() - self._start_marker.get_length()) / 2
        )
        self.add_draw_object(Position(0, start_marker_y_position), self._start_marker)

        start_marker_y_position = (
            0
            if self._end_marker.get_length() >= self._start_marker.get_length()
            else (self._start_marker.get_length() - self._end_marker.get_length()) / 2
        )

        self.add_draw_object(
            Position(self._length, start_marker_y_position),
            self._end_marker,
        )
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
