from dataclasses import asdict

from musurgia.graphics.drawobject import Container, Position
from musurgia.graphics.line_segment import (
    LineSegment,
    LineSegmentOptions,
    MarkerOptions,
)
from musurgia.graphics.models import LineOrientation


class SegmentedLine(Container):
    def __init__(
        self,
        *,
        type: LineOrientation,
        segment_lengths: list[int | float],
        marker_length: int | float | None = None,
        color: str | None = None,
        thickness: float | None = None,
        options: dict[int, LineSegmentOptions] | None = None,
    ) -> None:
        super().__init__()
        self.type = type
        self._segment_lengths = segment_lengths or []
        self._marker_length = marker_length
        self._color = color
        self._thickness = thickness
        self._options = options
        self._build()

    def _build_line_segments(self) -> list[LineSegment]:
        _line_segments = []
        for index, len in enumerate(self._segment_lengths):

            options = None

            if self._options:
                if line_segment_options := self._options.get(index + 1):
                    options = line_segment_options

            if not options:
                options = LineSegmentOptions(
                    start_marker=MarkerOptions(
                        length=self._marker_length or MarkerOptions.length
                    ),
                    end_marker=MarkerOptions(
                        length=self._marker_length or MarkerOptions.length
                    ),
                )

            if len == self._segment_lengths[-1]:
                ls = LineSegment(
                    type=self.type,
                    length=len,
                    color=self._color,
                    thickness=self._thickness,
                    options=asdict(options),
                    no_end_marker=False,
                )
            else:
                ls = LineSegment(
                    type=self.type,
                    length=len,
                    color=self._color,
                    thickness=self._thickness,
                    options=asdict(options),
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
            current_x = 0.0
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
            current_y = 0.0
            for ls in line_segments:
                position = Position(
                    max_straight_line_fix_position
                    - ls.get_straight_line(positioned=True)[0].x,
                    current_y,
                )
                self.add_draw_object(position=position, draw_object=ls)
                current_y += ls.get_length()

    def get_line_segments(self) -> list[LineSegment]:
        return [o for o in self.get_draw_objects() if isinstance(o, LineSegment)]

    def get_positioned_line_segments(self) -> list[tuple[Position, LineSegment]]:
        return [
            (p, o)
            for (p, o) in self.get_positioned_draw_objects()
            if isinstance(o, LineSegment)
        ]

    def get_length(self) -> float | int:
        return sum([sl.get_length() for sl in self.get_line_segments()])
