from dataclasses import dataclass, field
from typing import Any, Mapping

from musurgia.graphics.drawobject import Container, Position
from musurgia.graphics.line_segment import HorizontalLineSegment
from musurgia.graphics.util import overrides_data_class_options


@dataclass
class UnitMarkerOptions:
    length: float = 6.0


@dataclass
class UnitDivisionMarkerOptions:
    length: float = 3.0


@dataclass
class RulerOptions:
    unit_marker: UnitMarkerOptions = field(default_factory=UnitMarkerOptions)
    unit_division_marker: UnitDivisionMarkerOptions = field(
        default_factory=UnitDivisionMarkerOptions
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
        self._color = color
        self._thickness = thickness
        self._ruler_units: list[RulerUnit]
        self._options = RulerOptions()
        if options:
            overrides_data_class_options(self._options, options)
        self._build()

    def _build(self) -> None:
        self._create_ruler_units()
        for i, ru in enumerate(self._ruler_units):
            self.add_draw_object(Position(i * ru._length, 0), ru)

    def _create_ruler_units(self) -> None:
        number_of_units = int(self._length / self._unit_length)
        self._ruler_units = [
            RulerUnit(
                length=self._unit_length,
                division=self._unit_division,
                large_markers_length=self._options.unit_marker.length,
                small_markers_length=self._options.unit_division_marker.length,
                thickness=self._thickness,
                color=self._color,
            )
            for _ in range(number_of_units)
        ]
