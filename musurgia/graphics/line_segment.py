from musurgia.graphics.drawobject import (
    Container,
    Padding,
    Position,
    StraightLineDrawObject,
    TextDrawObject,
)

from dataclasses import dataclass, field, asdict, fields
from typing import Any, Literal, Mapping, cast, overload

from musurgia.graphics.models import LineOrientation
from musurgia.graphics.util import (
    overrides_data_class_options,
    toggle_line_orientation,
    toggle_position,
)


class Label(TextDrawObject):
    def __init__(
        self,
        *,
        text: str,
        offset: float | int = 0,
        padding: Padding = Padding(),
        font_family: str = "DejaVu Sans",
        font_size: int | float = 12,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            text=text,
            padding=padding,
            font_family=font_family,
            font_size=font_size,
            **kwargs,
        )
        self._offset = offset

    def get_offset(self) -> float | int:
        return self._offset


@dataclass
class MarkerOptions:
    length: float = 6.0
    thickness: float = 0.1
    color: str = "black"
    labels: list[Label] = field(default_factory=lambda: [])


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
        self.type = type
        self._options = MarkerOptions()
        if options:
            overrides_data_class_options(self._options, options)
        self._line: StraightLineDrawObject
        self._build()

    def _build(self) -> None:
        print(self._options)
        options = asdict(self._options)
        labels = options.pop("labels")

        labels.sort(key=lambda label: label.get_offset(), reverse=True)

        self._line = StraightLineDrawObject(type=self.type, **options)

        if labels:
            line_position = Position(0, labels[0].get_offset())
            if self.type == LineOrientation.HORIZONTAL:
                line_position = toggle_position(line_position)
        else:
            line_position = Position(0, 0)

        self.add_draw_object(line_position, self._line)

        for label in labels:
            position = Position(0, labels[0].get_offset()) - Position(
                0, label.get_offset()
            )
            if self.type == LineOrientation.HORIZONTAL:
                position = toggle_position(position)
            self.add_draw_object(position, label)

    def get_labels(self) -> list[Label]:
        return [do for do in self.get_draw_objects() if isinstance(do, Label)]

    def get_type(self) -> str:
        return self.type.value

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
        self._straight_line: StraightLineDrawObject
        self._start_marker: Marker
        self._end_marker: Marker | None

        self._build()

    def _build(self) -> None:
        self._start_marker = Marker(
            type=toggle_line_orientation(self.type),
            options=asdict(self._options.start_marker),
        )

        if not self._no_end_marker:
            self._end_marker = Marker(
                type=toggle_line_orientation(self.type),
                options=asdict(self._options.end_marker),
            )
        else:
            self._end_marker = None

        self._straight_line = StraightLineDrawObject(
            type=self.type, length=self._length, **asdict(self._options.straight_line)
        )

        start_marker_position = Position(
            0,
            (
                0
                if not self._end_marker
                or self._start_marker.get_length() >= self._end_marker.get_length()
                else (self._end_marker.get_length() - self._start_marker.get_length())
                / 2
            ),
        )

        end_marker_position = Position(
            self._length,
            (
                0
                if not self._end_marker
                or self._end_marker.get_length() >= self._start_marker.get_length()
                else (self._start_marker.get_length() - self._end_marker.get_length())
                / 2
            ),
        )

        straight_line_position = (
            Position(
                0,
                max(self._end_marker.get_length(), self._start_marker.get_length()) / 2,
            )
            if self._end_marker
            else Position(0, self._start_marker.get_length() / 2)
        )

        if self.type.value == "vertical":
            end_marker_position = toggle_position(end_marker_position)
            start_marker_position = toggle_position(start_marker_position)
            straight_line_position = toggle_position(straight_line_position)

        self.add_draw_object(start_marker_position, self._start_marker)

        if self._end_marker:
            self.add_draw_object(
                end_marker_position,
                self._end_marker,
            )

        self.add_draw_object(
            straight_line_position,
            self._straight_line,
        )

    @overload
    def get_markers(self) -> tuple[Marker, Marker | None]: ...

    @overload
    def get_markers(
        self, positioned: Literal[False]
    ) -> tuple[Marker, Marker | None]: ...

    @overload
    def get_markers(
        self, positioned: Literal[True]
    ) -> tuple[tuple[Position, Marker], tuple[Position, Marker] | None]: ...

    def get_markers(
        self, positioned: bool = False
    ) -> (
        tuple[Marker, Marker | None]
        | tuple[tuple[Position, Marker], tuple[Position, Marker] | None]
    ):
        if not positioned:
            return self._start_marker, self._end_marker
        else:
            positioned_start = [
                (p, cast(Marker, o))
                for (p, o) in self.get_draw_objects(positioned=True)
                if o == self._start_marker
            ][0]

            positioned_end = None
            if self._end_marker:
                positioned_end = [
                    (p, cast(Marker, o))
                    for (p, o) in self.get_draw_objects(positioned=True)
                    if o == self._end_marker
                ][0]

            return (positioned_start, positioned_end)

    @overload
    def get_straight_line(
        self, positioned: Literal[False] = False
    ) -> StraightLineDrawObject: ...

    @overload
    def get_straight_line(
        self, positioned: Literal[True]
    ) -> tuple[Position, StraightLineDrawObject]: ...

    def get_straight_line(
        self, positioned: bool = False
    ) -> StraightLineDrawObject | tuple[Position, StraightLineDrawObject]:
        if not positioned:
            return self._straight_line
        return [
            (p, cast(StraightLineDrawObject, o))
            for (p, o) in self.get_draw_objects(positioned=True)
            if o == self._straight_line
        ][0]

    def get_length(self) -> float:
        return self.get_straight_line().get_length()
