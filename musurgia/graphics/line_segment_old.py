from decimal import Decimal

from musurgia.graphics.container import Container
from musurgia.graphics.defaults import DEFAULT_COLOR
from musurgia.graphics.geometry import Position, Scalar
from musurgia.graphics.drawobject import (
    OldStraightLineDrawObject,
    Text,
    TextOptions,
)

from dataclasses import dataclass, field, asdict, fields
from typing import Any, Literal, Mapping, cast, overload

from musurgia.graphics.geometry import LineOrientation
from musurgia.graphics.util import (
    overrides_data_class_options,
    toggle_line_orientation,
    toggle_position,
)


class OldLabel(Text):
    def __init__(
        self,
        *,
        text: str,
        offset: tuple[Scalar, Scalar] = (0, 0),
        font_family: str = "DejaVu Sans",
        font_size: Scalar = 12,
        color: str = DEFAULT_COLOR,
    ) -> None:
        super().__init__(
            text=text,
            options=TextOptions(
                font_family=font_family, font_size=font_size, color=color
            ),
        )
        self._offset = offset

    def get_offset(self) -> tuple[Scalar, Scalar]:
        return self._offset


@dataclass
class MarkerOptions:
    length: Scalar = Decimal("6.0")
    thickness: Scalar = Decimal("0.1")
    color: str = "black"
    labels: list[OldLabel] = field(default_factory=lambda: [])


@dataclass
class StraightLineOptions:
    thickness: Scalar = Decimal("0.1")
    color: str = "black"


@dataclass
class LineSegmentOptions:
    start_marker: MarkerOptions = field(default_factory=MarkerOptions)
    end_marker: MarkerOptions = field(default_factory=MarkerOptions)
    straight_line: StraightLineOptions = field(default_factory=StraightLineOptions)


class OldMarker(Container):
    def __init__(
        self,
        *,
        type: LineOrientation,
        options: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__()
        self.type = type
        self._options = MarkerOptions()
        if options:
            overrides_data_class_options(self._options, options)
        self._line: OldStraightLineDrawObject
        self._build()

    def _build(self) -> None:
        options = asdict(self._options)
        labels = cast(list[OldLabel], options.pop("labels"))

        labels.sort(key=lambda label: label.get_offset()[1], reverse=True)

        self._line = OldStraightLineDrawObject(type=self.type, **options)

        if labels:
            first_label = labels[0]
            line_position = Position(0, first_label.get_offset()[1])
            if self.type == LineOrientation.HORIZONTAL:
                line_position = toggle_position(line_position)
        else:
            line_position = Position(0, 0)

        self.add_draw_object(line_position, self._line)

        if labels:
            first_label = labels[0]
            for label in labels:
                position = Position.from_values(
                    *first_label.get_offset()
                ) - Position.from_values(*label.get_offset())

                if self.type == LineOrientation.HORIZONTAL:
                    position = toggle_position(position)
                self.add_draw_object(position, label)

    def get_labels(self) -> list[OldLabel]:
        return [do for do in self.get_draw_objects() if isinstance(do, OldLabel)]

    def get_type(self) -> str:
        return self.type.value

    def get_length(self) -> Scalar:
        return self._line.get_length()

    def get_thickness(self) -> Scalar:
        return self._line.thickness

    def get_color(self) -> str:
        return self._line.color

    @overload
    def get_line(self) -> OldStraightLineDrawObject: ...

    @overload
    def get_line(self, *, positioned: Literal[False]) -> OldStraightLineDrawObject: ...

    @overload
    def get_line(
        self, *, positioned: Literal[True]
    ) -> tuple[Position, OldStraightLineDrawObject]: ...

    def get_line(
        self, *, positioned: bool = False
    ) -> OldStraightLineDrawObject | tuple[Position, OldStraightLineDrawObject]:
        positioned_line = [
            (p, cast(OldStraightLineDrawObject, o))
            for (p, o) in self.get_draw_objects(positioned=True)
            if o == self._line
        ][0]
        if positioned:
            return positioned_line
        return positioned_line[1]

    def get_middle_of_line_coordinate(self) -> Scalar:
        position, line = self.get_line(positioned=True)
        if self.type.value == "vertical":
            return position.y + line.get_length() / 2
        else:
            return position.x + line.get_length() / 2


class OldLineSegment(Container):
    def __init__(
        self,
        *,
        type: LineOrientation,
        length: Scalar,
        color: str | None = None,
        thickness: Scalar | None = None,
        options: Mapping[str, Any] | None = None,
        no_end_marker: bool = False,
    ) -> None:
        super().__init__()
        self.type = type
        self._length = length
        self._options = LineSegmentOptions()
        self._no_end_marker = no_end_marker

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
        self._straight_line: OldStraightLineDrawObject
        self._start_marker: OldMarker
        self._end_marker: OldMarker | None

        self._build()

    def _calculate_start_marker_position(self) -> Position:
        p = Position(
            0,
            (
                0
                if not self._end_marker
                or self._start_marker.get_middle_of_line_coordinate()
                >= self._end_marker.get_middle_of_line_coordinate()
                else (
                    self._end_marker.get_middle_of_line_coordinate()
                    - self._start_marker.get_middle_of_line_coordinate()
                )
            ),
        )
        p = p + Position(Decimal(self._start_marker.get_thickness()) / Decimal("2"), 0)
        if self.type.value == "vertical":
            p = toggle_position(p)
        return p

    def _calculate_end_marker_position(self) -> Position:
        p = Position(
            self._length,
            (
                0
                if not self._end_marker
                or self._end_marker.get_middle_of_line_coordinate()
                >= self._start_marker.get_middle_of_line_coordinate()
                else (
                    self._start_marker.get_middle_of_line_coordinate()
                    - self._end_marker.get_middle_of_line_coordinate()
                )
            ),
        )
        if self._end_marker:
            p = p - Position(
                Decimal(self._end_marker.get_thickness()) / Decimal("2"), 0
            )
        if self.type.value == "vertical":
            p = toggle_position(p)
        return p

    def _calculate_straight_line_position(self) -> Position:
        p = (
            Position(
                0,
                max(
                    self._end_marker.get_middle_of_line_coordinate(),
                    self._start_marker.get_middle_of_line_coordinate(),
                ),
            )
            if self._end_marker
            else Position(0, self._start_marker.get_middle_of_line_coordinate())
        )
        if self.type.value == "vertical":
            p = toggle_position(p)
        return p

    def _build(self) -> None:
        self._start_marker = OldMarker(
            type=toggle_line_orientation(self.type),
            options=asdict(self._options.start_marker),
        )

        if not self._no_end_marker:
            self._end_marker = OldMarker(
                type=toggle_line_orientation(self.type),
                options=asdict(self._options.end_marker),
            )
        else:
            self._end_marker = None

        self._straight_line = OldStraightLineDrawObject(
            type=self.type, length=self._length, **asdict(self._options.straight_line)
        )

        self.add_draw_object(
            self._calculate_start_marker_position(), self._start_marker
        )

        if self._end_marker:
            self.add_draw_object(
                self._calculate_end_marker_position(),
                self._end_marker,
            )

        self.add_draw_object(
            self._calculate_straight_line_position(),
            self._straight_line,
        )

    @overload
    def get_markers(self) -> tuple[OldMarker, OldMarker | None]: ...

    @overload
    def get_markers(
        self, positioned: Literal[False]
    ) -> tuple[OldMarker, OldMarker | None]: ...

    @overload
    def get_markers(
        self, positioned: Literal[True]
    ) -> tuple[tuple[Position, OldMarker], tuple[Position, OldMarker] | None]: ...

    def get_markers(
        self, positioned: bool = False
    ) -> (
        tuple[OldMarker, OldMarker | None]
        | tuple[tuple[Position, OldMarker], tuple[Position, OldMarker] | None]
    ):
        if not positioned:
            return self._start_marker, self._end_marker
        else:
            positioned_start = [
                (p, cast(OldMarker, o))
                for (p, o) in self.get_draw_objects(positioned=True)
                if o == self._start_marker
            ][0]

            positioned_end = None
            if self._end_marker:
                positioned_end = [
                    (p, cast(OldMarker, o))
                    for (p, o) in self.get_draw_objects(positioned=True)
                    if o == self._end_marker
                ][0]

            return (positioned_start, positioned_end)

    def get_labels(self) -> list[OldLabel]:
        return [
            label
            for marker in self.get_markers()
            if marker
            for label in marker.get_labels()
        ]

    @overload
    def get_straight_line(
        self, positioned: Literal[False] = False
    ) -> OldStraightLineDrawObject: ...

    @overload
    def get_straight_line(
        self, positioned: Literal[True]
    ) -> tuple[Position, OldStraightLineDrawObject]: ...

    def get_straight_line(
        self, positioned: bool = False
    ) -> OldStraightLineDrawObject | tuple[Position, OldStraightLineDrawObject]:
        if not positioned:
            return self._straight_line
        return [
            (p, cast(OldStraightLineDrawObject, o))
            for (p, o) in self.get_draw_objects(positioned=True)
            if o == self._straight_line
        ][0]

    def get_length(self) -> Scalar:
        return self.get_straight_line().get_length()
