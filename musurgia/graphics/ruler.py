from dataclasses import dataclass, field, fields
from typing import Any, Mapping

from musurgia.graphics.drawobject import Container, Position
from musurgia.graphics.line_segment import HorizontalLineSegment
from musurgia.graphics.util import overrides_data_class_options


@dataclass
class UnitMarkerOptions:
    length: float = 6.0
    thickness: float = 0.2
    color: str = "black"


@dataclass
class UnitDivisionMarkerOptions:
    length: float = 3.0
    thickness: float = 0.1
    color: str = "black"


@dataclass
class UnitStraightLineOptions:
    thickness: float = 0.2
    color: str = "black"


@dataclass
class RulerOptions:
    unit_marker: UnitMarkerOptions = field(default_factory=UnitMarkerOptions)
    unit_division_marker: UnitDivisionMarkerOptions = field(
        default_factory=UnitDivisionMarkerOptions
    )
    straight_line: UnitStraightLineOptions = field(
        default_factory=UnitStraightLineOptions
    )


class RulerUnit(Container):
    def __init__(
        self,
        *,
        length: float | int,
        division: int,
        large_markers_length: float | int,
        small_markers_length: float | int,
        color: str | None = None,
        thickness: float | None = None,
    ):
        super().__init__()
        self._length = length
        self._division = division
        self._large_markers_length = large_markers_length
        self._small_markers_length = small_markers_length
        self._color = color
        self._thickness = thickness
        self._build()

    def _build(self) -> None:
        unit_division_length = self._length / self._division
        for index in range(self._division):
            x_position = index * unit_division_length
            y_position = (
                0
                if index in [0, self._division - 1]
                else (self._large_markers_length - self._small_markers_length) / 2
            )
            options: Any = {"start_marker": {}, "end_marker": {}}
            if index == 0:
                options["start_marker"]["length"] = self._large_markers_length
                options["end_marker"]["length"] = self._small_markers_length
                if self._thickness:
                    options["start_marker"]["thickness"] = self._thickness
                    options["end_marker"]["thickness"] = self._thickness / 2

            elif index == self._division - 1:
                options["start_marker"]["length"] = self._small_markers_length
                options["end_marker"]["length"] = self._large_markers_length
                if self._thickness:
                    options["start_marker"]["thickness"] = self._thickness / 2
                    options["end_marker"]["thickness"] = self._thickness
            else:
                options["start_marker"]["length"] = self._small_markers_length
                options["end_marker"]["length"] = self._small_markers_length
                if self._thickness:
                    options["start_marker"]["thickness"] = self._thickness / 2
                    options["end_marker"]["thickness"] = self._thickness / 2

            hls = HorizontalLineSegment(
                length=unit_division_length,
                color=self._color,
                thickness=self._thickness,
                options=options,
            )
            hls._end_marker.show = False

            self.add_draw_object(
                Position(x_position, y_position),
                hls,
            )


class HorizontalRuler(Container):
    def __init__(
        self,
        *,
        length: float,
        unit_length: int | float = 10,
        unit_division: int = 10,
        color: str | None = None,
        thickness: float | None = None,
        options: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__()
        self._length = length
        self._unit_length = unit_length
        self._unit_division = unit_division
        self._options = RulerOptions()
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

        self._ruler_units: list[RulerUnit]

        self._build()

    def _build(self) -> None:
        pass
