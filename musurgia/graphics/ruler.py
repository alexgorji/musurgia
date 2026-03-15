from dataclasses import dataclass, field
from typing import Any, Mapping

from musurgia.graphics.drawobject import Container, Position, TextDrawObject
from musurgia.graphics.line_segment import HorizontalLineSegment, Marker
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
        labels_interval: int = 1,
        label_offset=Position(1, 3),
        color: str | None = None,
        thickness: float | None = None,
        options: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__()
        self._length = length
        self._unit_length = unit_length
        self._unit_division = unit_division
        self._labels_interval = labels_interval
        self._label_offset = label_offset
        self._color = color
        self._thickness = thickness
        self._options = RulerOptions()
        if options:
            overrides_data_class_options(self._options, options)
        self._build()

    def _build(self) -> None:
        self._build_ruler_units()
        self._build_labels()

    def _build_ruler_units(self):
        self._create_ruler_units()
        for p, ru in zip(self._get_ruler_unit_positions(), self._ruler_units):
            self.add_draw_object(p, ru)

    def _build_labels(self):
        for i, (p, _) in enumerate(self.get_positioned_ruler_units()):
            if i % self._labels_interval == 0:
                self.add_draw_object(
                    Position(p.x + self._label_offset.x, 0),
                    TextDrawObject(text=str(i), color=self._color),
                )

    def _create_ruler_units(self) -> None:
        self._ruler_units = [
            RulerUnit(
                length=self._unit_length,
                division=self._unit_division,
                large_markers_length=self._options.unit_marker.length,
                small_markers_length=self._options.unit_division_marker.length,
                thickness=self._thickness,
                color=self._color,
            )
            for _ in range(self._get_number_ruler_units())
        ]

    def _get_division_size(self):
        return self._unit_length / self._unit_division

    def _get_ruler_unit_positions(self):
        return [
            Position(i * self._unit_length, self._label_offset.y)
            for i in range(self._get_number_ruler_units())
        ]

    def _get_number_ruler_units(self):
        return int(self._length / self._unit_length)

    def get_positioned_ruler_units(self):
        return [
            (p, o)
            for (p, o) in self.get_positioned_draw_objects()
            if isinstance(o, RulerUnit)
        ]

    def get_positioned_markers(self):
        return [
            (rup + lp + mp, m)
            for (rup, ru) in self.get_positioned_ruler_units()
            for (lp, l) in [
                (p, o)
                for (p, o) in ru.get_positioned_draw_objects()
                if isinstance(o, HorizontalLineSegment)
            ]
            for (mp, m) in [
                (pp, oo)
                for (pp, oo) in l.get_positioned_draw_objects()
                if isinstance(oo, Marker) and oo.show
            ]
        ]

    def get_positioned_labels(self):
        return [
            (p, o)
            for p, o in self.get_positioned_draw_objects()
            if isinstance(o, TextDrawObject)
        ]
