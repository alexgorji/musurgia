from dataclasses import dataclass, field
from typing import Any, Mapping


from musurgia.graphics.container import Container
from musurgia.graphics.line_segment import Label
from musurgia.graphics.geometry import LineOrientation
from musurgia.graphics.segmented_line import SegmentedLine
from musurgia.graphics.util import overrides_data_class_options


@dataclass
class UnitMarkerOptions:
    length: float = 6.0
    thickness: float = 0.5


@dataclass
class UnitDivisionMarkerOptions:
    length: float = 3.0
    thickness: float = 0.5


@dataclass
class RulerLabelOptions:
    offset: tuple[int | float, int | float] = (1, 3)
    color: str = "black"
    font_family: str = "DejaVu Sans"
    font_size: int | float = 10


@dataclass
class RulerOptions:
    unit_marker: UnitMarkerOptions = field(default_factory=UnitMarkerOptions)
    unit_division_marker: UnitDivisionMarkerOptions = field(
        default_factory=UnitDivisionMarkerOptions
    )
    unit_length: int | float = 10
    unit_division: int = 10
    labels_interval: int = 1
    label: RulerLabelOptions = field(default_factory=RulerLabelOptions)
    thickness: float = 1


def _get_division_length(ruler_options: RulerOptions) -> int | float:
    return ruler_options.unit_length / ruler_options.unit_division


def _get_number_of_units(
    ruler_options: RulerOptions, length: int | float
) -> int | float:
    return length / ruler_options.unit_length


def _get_number_of_divisions(ruler_options: RulerOptions, length: int | float) -> int:
    return int(
        _get_number_of_units(ruler_options, length) * ruler_options.unit_division
    )


def _ruler_segment_lengths(
    ruler_options: RulerOptions, length: int | float
) -> list[int | float]:
    number_of_divisions = _get_number_of_divisions(ruler_options, length)
    division_length = _get_division_length(ruler_options)
    return [division_length for _ in range(number_of_divisions)]


def _create_segmented_line_options(
    ruler_options: RulerOptions, length: int | float
) -> dict[int, Mapping[str, Any]]:
    options: dict[int, Any] = {}
    number_of_divisions = _get_number_of_divisions(ruler_options, length)
    for index in range(number_of_divisions):
        key = index + 1
        options[key] = {}
        if index % ruler_options.unit_division == 0:
            index_of_unit = index / ruler_options.unit_division
            options[key]["start_marker"] = {
                "length": ruler_options.unit_marker.length,
                "thickness": ruler_options.unit_marker.thickness,
            }
            if index_of_unit % ruler_options.labels_interval == 0:
                options[key]["start_marker"]["labels"] = [
                    Label(
                        text=str(int(index_of_unit) + 1),
                        color=ruler_options.label.color,
                        font_size=ruler_options.label.font_size,
                        font_family=ruler_options.label.font_family,
                        offset=ruler_options.label.offset,
                    )
                ]
        else:
            options[key]["start_marker"] = {
                "thickness": ruler_options.unit_marker.thickness,
            }
        if index == number_of_divisions - 1:
            options[key]["end_marker"] = {
                "thickness": ruler_options.unit_marker.thickness
            }
            if (index + 1) % ruler_options.unit_division == 0:
                options[key]["end_marker"]["length"] = ruler_options.unit_marker.length
    return options


class Ruler(Container):
    def __init__(
        self,
        *,
        type: LineOrientation,
        length: float,
        color: str | None = None,
        options: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__()
        ruler_options = RulerOptions()
        if options:
            overrides_data_class_options(ruler_options, options)

        segmented_line_options = _create_segmented_line_options(ruler_options, length)

        segment_lengths = _ruler_segment_lengths(ruler_options, length)

        self._segmented_line = SegmentedLine(
            type=type,
            segment_lengths=segment_lengths,
            marker_length=ruler_options.unit_division_marker.length,
            color=color,
            thickness=ruler_options.thickness,
            options=segmented_line_options,
        )

        self._build()

    def _build(self) -> None:
        for p, o in self._segmented_line.get_draw_objects(positioned=True):
            self.add_draw_object(p, o)
