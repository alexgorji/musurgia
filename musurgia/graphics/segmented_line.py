from dataclasses import asdict

from musurgia.graphics.drawobject import Container, Position
from musurgia.graphics.line_segment import (
    LineSegment,
    LineSegmentOptions,
    MarkerOptions,
)
from musurgia.graphics.models import LineOrientation
from musurgia.graphics.util import toggle_position


class SegmentedLine(Container):
    def __init__(
        self,
        *,
        type: LineOrientation,
        segment_lengths: list[int | float] | None = None,
        marker_length: int | float | None = None,
        color: str | None = None,
        thickness: float | None = None,
    ) -> None:
        super().__init__()
        self.type = type
        self._segment_lengths = segment_lengths or []
        self._marker_length = marker_length
        self._color = color
        self._thickness = thickness
        self._build()

    def _build(self) -> None:
        h_position = Position(0, 0)
        for len in self._segment_lengths:
            if self.type.value == "horizontal":
                position = h_position
            else:
                position = toggle_position(h_position)

            options = LineSegmentOptions(
                start_marker=MarkerOptions(
                    length=self._marker_length or MarkerOptions.length
                ),
                end_marker=MarkerOptions(
                    length=self._marker_length or MarkerOptions.length
                ),
            )

            do = LineSegment(
                type=self.type,
                length=len,
                color=self._color,
                thickness=self._thickness,
                options=asdict(options),
            )
            _, end = do.get_markers()

            if len == self._segment_lengths[-1]:
                end.show = True
            else:
                end.show = False

            self.add_draw_object(position=position, draw_object=do)
            h_position = Position(h_position.x + len, 0)

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
