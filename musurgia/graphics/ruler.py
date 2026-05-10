from dataclasses import dataclass, field
from decimal import Decimal


from musurgia.graphics.defaults import DEFAULT_COLOR, DEFAULT_THICKNESS
from musurgia.graphics.container import Container
from musurgia.graphics.drawobject import LineOptions
from musurgia.graphics.geometry import LineOrientation, Position, Scalar
from musurgia.graphics.segmented_line import LineSegment, Marker, SegmentedLine, Label
from musurgia.graphics.util import (
    convert_to_scalar,
    toggle_line_orientation,
)


@dataclass
class UnitMarkerOptions:
    length: Scalar = Decimal("6.0")
    options = LineOptions()


@dataclass
class UnitDivisionMarkerOptions:
    length: Scalar = Decimal("3.0")
    options = LineOptions(thickness=convert_to_scalar(DEFAULT_THICKNESS / 2))


@dataclass
class RulerLabelOptions:
    offset: tuple[Scalar, Scalar] = (1, 3)
    color: str = "black"
    font_family: str = "DejaVu Sans"
    font_size: Scalar = 10


@dataclass
class RulerOptions:
    unit_marker: UnitMarkerOptions = field(default_factory=UnitMarkerOptions)
    unit_division_marker: UnitDivisionMarkerOptions = field(
        default_factory=UnitDivisionMarkerOptions
    )
    unit_length: Scalar = 10
    unit_division: int = 10
    labels_interval: int = 1
    label: RulerLabelOptions = field(default_factory=RulerLabelOptions)
    thickness: Scalar = DEFAULT_THICKNESS
    color: str = DEFAULT_COLOR


def _get_division_length(ruler_options: RulerOptions) -> Decimal:
    return Decimal(ruler_options.unit_length) / Decimal(ruler_options.unit_division)


class Ruler(Container):
    def __init__(
        self,
        *,
        type: LineOrientation,
        length: Scalar,
        options: RulerOptions | None = None,
    ) -> None:
        super().__init__()
        self.type = type
        self.options = options or RulerOptions()
        self.length = length
        self._units: list[SegmentedLine] = []
        self._segmented_line = SegmentedLine(type=self.type)
        self._populate_segmented_line()

    def _populate_segmented_line(self) -> None:
        self._segmented_line.remove_line_segments()

        current_length = Decimal("0")
        unit_index = 0
        while current_length < self.length:
            unit = SegmentedLine(type=self.type)

            number_of_divisions = self.options.unit_division
            division_length = _get_division_length(self.options)

            if number_of_divisions * division_length + current_length > self.length:
                number_of_divisions = int(self.length - current_length)
            for i in range(number_of_divisions):
                if i == 0:
                    start_marker = Marker(
                        type=toggle_line_orientation(self.type),
                        length=self.options.unit_marker.length,
                        options=self.options.unit_marker.options,
                    )
                    label = Label(text=str(unit_index + 1))
                    if self.type == LineOrientation.HORIZONTAL:
                        label.offset = Position(
                            0,
                            label.size.height,
                        )
                    else:
                        label.offset = Position(label.size.width, 0)
                    start_marker.add_label(label)
                else:
                    start_marker = Marker(
                        type=toggle_line_orientation(self.type),
                        length=self.options.unit_division_marker.length,
                        options=self.options.unit_division_marker.options,
                    )
                ls = LineSegment(
                    type=self.type,
                    length=division_length,
                    start_marker=start_marker,
                    options=LineOptions(
                        thickness=self.options.thickness, color=self.options.color
                    ),
                )

                unit.add_line_segment(ls)
            unit_index += 1
            current_length += unit.get_length()
            self._units.append(unit)
            for ls in unit.get_line_segments():
                self._segmented_line.add_line_segment(ls)

    def build(self) -> None:
        self.as_segmented_line().build()
        self.add_draw_object(Position(0, 0), self.as_segmented_line())

    def get_units(self) -> list[SegmentedLine]:
        return self._units

    def as_segmented_line(self) -> SegmentedLine:
        return self._segmented_line
