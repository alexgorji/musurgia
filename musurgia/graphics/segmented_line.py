from decimal import Decimal
from typing import Any, Literal, Mapping, overload

from musurgia.graphics.container import Container
from musurgia.graphics.geometry import Position, LineOrientation, Scalar
from musurgia.graphics.line_segment import (
    Label,
    LineSegment,
)
from musurgia.graphics.util import override_options_mappings


class SegmentedLine(Container):
    def __init__(
        self,
        *,
        type: LineOrientation,
        segment_lengths: list[Scalar],
        marker_length: Scalar | None = None,
        show_last_end_marker: bool = True,
        color: str | None = None,
        thickness: Scalar | None = None,
        options: dict[int, Mapping[str, Any]] | None = None,
    ) -> None:
        super().__init__()
        self.type = type
        self._segment_lengths = segment_lengths or []
        self._marker_length = marker_length
        self._show_last_end_marker = show_last_end_marker
        self._color = color
        self._thickness = thickness
        self._options = options
        self._build()

    def _build_line_segments(self) -> list[LineSegment]:
        _line_segments = []
        for index, length in enumerate(self._segment_lengths):

            options: dict[str, Any] = {
                "start_marker": {},
                "end_marker": {},
                "straight_line": {},
            }

            if self._marker_length:
                options["start_marker"]["length"] = self._marker_length
                options["end_marker"]["length"] = self._marker_length

            if self._options:
                if override := self._options.get(index + 1):
                    options = override_options_mappings(options, override)
                elif index == len(self._segment_lengths) - 1:
                    if override := self._options.get(-1):
                        options = override_options_mappings(options, override)

            if index == len(self._segment_lengths) - 1:
                # if index == len(self._segment_lengths) - 1 and self._show_last_end_marker:
                ls = LineSegment(
                    type=self.type,
                    length=length,
                    color=self._color,
                    thickness=self._thickness,
                    options=options,
                    no_end_marker=False,
                )
            else:
                ls = LineSegment(
                    type=self.type,
                    length=length,
                    color=self._color,
                    thickness=self._thickness,
                    options=options,
                    no_end_marker=True,
                )
            _line_segments.append(ls)
        return _line_segments

    def _build(self) -> None:
        line_segments = self._build_line_segments()
        if self.type.value == "horizontal":
            max_straight_line_fix_position = max(
                [ls.get_straight_line(positioned=True)[0].y for ls in line_segments]
            )
            current_x = Decimal(0)
            for ls in line_segments:
                position = Position(
                    current_x,
                    max_straight_line_fix_position
                    - ls.get_straight_line(positioned=True)[0].y,
                )
                self.add_draw_object(position=position, draw_object=ls)
                current_x += ls.get_length()
        else:
            max_straight_line_fix_position = max(
                [ls.get_straight_line(positioned=True)[0].x for ls in line_segments]
            )
            current_y = Decimal(0)
            for ls in line_segments:
                position = Position(
                    max_straight_line_fix_position
                    - ls.get_straight_line(positioned=True)[0].x,
                    current_y,
                )
                self.add_draw_object(position=position, draw_object=ls)
                current_y += ls.get_length()

    def get_labels(self) -> list[Label]:
        return [label for ls in self.get_line_segments() for label in ls.get_labels()]

    @overload
    def get_line_segments(self) -> list[LineSegment]: ...

    @overload
    def get_line_segments(self, *, positioned: Literal[False]) -> list[LineSegment]: ...

    @overload
    def get_line_segments(
        self, *, positioned: Literal[True]
    ) -> list[tuple[Position, LineSegment]]: ...

    def get_line_segments(
        self, *, positioned: bool = False
    ) -> list[LineSegment] | list[tuple[Position, LineSegment]]:
        if not positioned:
            return [o for o in self.get_draw_objects() if isinstance(o, LineSegment)]
        else:
            return [
                (p, o)
                for (p, o) in self.get_draw_objects(positioned=True)
                if isinstance(o, LineSegment)
            ]

    def get_length(self) -> Scalar:
        return sum([sl.get_length() for sl in self.get_line_segments()])
