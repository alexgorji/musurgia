from musurgia.graphics.drawobject import (
    Container,
    Position,
    StraightLineDrawObject,
)

from dataclasses import dataclass, field, asdict, fields
from typing import Any, Mapping

from musurgia.graphics.models import LineOrientation
from musurgia.graphics.util import (
    overrides_data_class_options,
    toggle_line_orientation,
    toggle_position,
)


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
        type: LineOrientation,
        options: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__()
        self._type = type
        self._options = MarkerOptions()
        if options:
            overrides_data_class_options(self._options, options)
        self._line: StraightLineDrawObject
        self._build()

    def _build(self) -> None:
        self._line = StraightLineDrawObject(type=self._type, **asdict(self._options))

        self.add_draw_object(Position(0, 0), self._line)

    def get_type(self) -> str:
        return self._type.value

    def get_length(self) -> float:
        return self._line.get_length()

    def get_thickness(self) -> float:
        return self._line.thickness

    def get_color(self) -> str:
        return self._line.color


class LineSegment(Container):
    def __init__(
        self,
        *,
        type: LineOrientation,
        length: float,
        color: str | None = None,
        thickness: float | None = None,
        options: Mapping[str, Any] | None = None,
    ):
        super().__init__()
        self.type = type
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

        self._straight_line: StraightLineDrawObject
        self._start_marker: Marker
        self._end_marker: Marker

        self._build()

    def _build(self) -> None:
        self._start_marker = Marker(
            type=toggle_line_orientation(self.type),
            options=asdict(self._options.start_marker),
        )

        self._end_marker = Marker(
            type=toggle_line_orientation(self.type),
            options=asdict(self._options.end_marker),
        )

        self._straight_line = StraightLineDrawObject(
            type=self.type, length=self._length, **asdict(self._options.straight_line)
        )

        start_marker_position = Position(
            0,
            (
                0
                if self._start_marker.get_length() >= self._end_marker.get_length()
                else (self._end_marker.get_length() - self._start_marker.get_length())
                / 2
            ),
        )

        end_marker_position = Position(
            self._length,
            (
                0
                if self._end_marker.get_length() >= self._start_marker.get_length()
                else (self._start_marker.get_length() - self._end_marker.get_length())
                / 2
            ),
        )

        straight_line_position = Position(
            0,
            max(self._end_marker.get_length(), self._start_marker.get_length()) / 2,
        )

        if self.type.value == "vertical":
            end_marker_position = toggle_position(end_marker_position)
            start_marker_position = toggle_position(start_marker_position)
            straight_line_position = toggle_position(straight_line_position)

        self.add_draw_object(start_marker_position, self._start_marker)

        self.add_draw_object(
            end_marker_position,
            self._end_marker,
        )

        self.add_draw_object(
            straight_line_position,
            self._straight_line,
        )

    def get_markers(self) -> tuple[Marker, Marker]:
        return self._start_marker, self._end_marker

    def get_straight_line(self) -> StraightLineDrawObject:
        return self._straight_line
