from typing import Any, cast

from musurgia.graphics.geometry import (
    Coordinates,
    LineOrientation,
    Position,
    Scalar,
    Size,
)

from musurgia.graphics.container import Container
from musurgia.graphics.drawobject import DrawObject, TextDrawObject

from musurgia.graphics.util import (
    convert_to_scalar,
    toggle_line_orientation,
    toggle_position,
)

DEFAULT_COLOR = "blue"
DEFAULT_THICKNESS = 2
DEFAULT_MARKER_LENGTH = 10


class Label(TextDrawObject):
    def __init__(
        self,
        *,
        text: str,
        offset: Position = Position(0, 0),
        font_family: str = "DejaVu Sans",
        font_size: Scalar = 12,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            text=text,
            font_family=font_family,
            font_size=font_size,
            **kwargs,
        )
        self._offset = offset

    def get_offset(self) -> Position:
        return self._offset


class StraightLine(DrawObject):
    def __init__(
        self,
        *,
        type: LineOrientation,
        length: Scalar,
        color: str | None = None,
        thickness: Scalar | None = None,
    ) -> None:
        super().__init__()
        self.type = type
        self.length = length
        self.color = color or DEFAULT_COLOR
        self.thickness = thickness or DEFAULT_THICKNESS

    def get_bounding_box_coordinates(self):
        xmin = 0
        xmax = self.length
        ymin = 0
        ymax = self.thickness

        if self.type == LineOrientation.VERTICAL:
            xmax = self.thickness
            ymax = self.length

        return Coordinates(
            Position(xmin, ymin),
            Position(xmax, ymin),
            Position(xmax, ymax),
            Position(xmin, ymax),
        )

    @property
    def size(self) -> Size:
        coor = self.get_bounding_box_coordinates()
        return Size(coor.tr.x - coor.tl.x, coor.bl.y - coor.tl.y)


class Marker(Container):
    def __init__(
        self,
        *,
        type: LineOrientation,
        length: Scalar,
        labels: list[Label] | None = None,
        color: str | None = None,
        thickness: Scalar | None = None,
    ) -> None:
        super().__init__()
        self.type = type
        self._labels = labels or []
        self._line = StraightLine(
            type=self.type, length=length, color=color, thickness=thickness
        )

    def get_line_position(self) -> Position:
        labels = self.get_labels()
        if labels:
            first_label = cast(Label, self.get_first_label())
            if self.type == LineOrientation.HORIZONTAL:
                line_position = Position(first_label.get_offset().x, 0)
            else:
                line_position = Position(0, first_label.get_offset().y)
        else:
            line_position = Position(0, 0)
        return line_position

    def build(self) -> None:
        self.add_draw_object(self.get_line_position(), self._line)
        labels = self.get_labels()
        if labels:
            first_label = cast(Label, self.get_first_label())
            for label in labels:

                if self.type == LineOrientation.HORIZONTAL:
                    position = Position(
                        first_label.get_offset().x - label.get_offset().x,
                        label.get_offset().y,
                    )
                else:
                    position = Position(
                        label.get_offset().x,
                        first_label.get_offset().y - label.get_offset().y,
                    )
                self.add_draw_object(position, label)

    def get_first_label(self) -> Label | None:
        if not self.get_labels():
            return None
        if self.type == LineOrientation.HORIZONTAL:
            return max(self.get_labels(), key=lambda label: label.get_offset().x)
        return max(self.get_labels(), key=lambda label: label.get_offset().y)

    def get_labels(self) -> list[Label]:
        return self._labels

    def add_label(self, label: Label) -> Label:
        self._labels.append(label)
        # if self.type == LineOrientation.VERTICAL:
        #     self._labels.sort(key=lambda label: label.get_offset().y, reverse=True)
        # else:
        #     self._labels.sort(key=lambda label: label.get_offset().x, reverse=True)
        return label

    @property
    def color(self) -> str:
        return self._line.color

    @color.setter
    def color(self, value: str) -> None:
        self._line.color = value

    @property
    def thickness(self) -> Scalar:
        return self._line.thickness

    @thickness.setter
    def thickness(self, value: Scalar) -> None:
        self._line.thickness = value

    @property
    def length(self) -> Scalar:
        return self._line.length

    @length.setter
    def length(self, value: Scalar) -> None:
        self._line.length = value

    def get_line(self) -> StraightLine:
        return self._line

    def get_middle_of_line_coordinate(self) -> Scalar:
        position, line = self.get_line_position(), self.get_line()
        if self.type.value == "vertical":
            return position.y + convert_to_scalar(line.length / 2)
        else:
            return position.x + convert_to_scalar(line.length / 2)


class LineSegment(Container):
    def __init__(
        self,
        *,
        type: LineOrientation,
        length: Scalar,
        color: str | None = None,
        thickness: Scalar | None = None,
        start_marker: Marker | None = None,
        end_marker: Marker | None = None,
    ) -> None:
        super().__init__()
        self.type = type
        self._color = color
        self._thickness = thickness

        self._straight_line = StraightLine(
            type=self.type, length=length, color=color, thickness=thickness
        )
        self.start_marker = start_marker or Marker(
            type=toggle_line_orientation(type),
            length=DEFAULT_MARKER_LENGTH,
            color=self._color,
            thickness=convert_to_scalar(DEFAULT_THICKNESS / 2),
        )
        self.end_marker = end_marker

    def _calculate_start_marker_position(self) -> Position:
        p = Position(
            0,
            (
                0
                if not self.end_marker
                or self.start_marker.get_middle_of_line_coordinate()
                >= self.end_marker.get_middle_of_line_coordinate()
                else (
                    self.end_marker.get_middle_of_line_coordinate()
                    - self.start_marker.get_middle_of_line_coordinate()
                )
            ),
        )
        p = p + Position(convert_to_scalar(self.start_marker.thickness / 2), 0)
        if self.type.value == "vertical":
            p = toggle_position(p)
        return p

    def _calculate_end_marker_position(self) -> Position:
        p = Position(
            self.length,
            (
                0
                if not self.end_marker
                or self.end_marker.get_middle_of_line_coordinate()
                >= self.start_marker.get_middle_of_line_coordinate()
                else (
                    self.start_marker.get_middle_of_line_coordinate()
                    - self.end_marker.get_middle_of_line_coordinate()
                )
            ),
        )
        if self.end_marker:
            p = p - Position(convert_to_scalar(self.end_marker.thickness / 2), 0)
        if self.type.value == "vertical":
            p = toggle_position(p)
        return p

    def _calculate_straight_line_position(self) -> Position:
        p = (
            Position(
                0,
                max(
                    self.end_marker.get_middle_of_line_coordinate(),
                    self.start_marker.get_middle_of_line_coordinate(),
                ),
            )
            if self.end_marker
            else Position(0, self.start_marker.get_middle_of_line_coordinate())
        )
        if self.type.value == "vertical":
            p = toggle_position(p)
        return p

    def build(self) -> None:
        self.start_marker.build()

        self.add_draw_object(self._calculate_start_marker_position(), self.start_marker)

        if self.end_marker:
            self.end_marker.build()
            self.add_draw_object(
                self._calculate_end_marker_position(),
                self.end_marker,
            )

        self.add_draw_object(
            self._calculate_straight_line_position(),
            self._straight_line,
        )

    def add_end_maker(self, marker: Marker | None = None) -> Marker:
        self.end_marker = marker or Marker(
            type=toggle_line_orientation(self.type),
            length=DEFAULT_MARKER_LENGTH,
            color=self._color,
            thickness=convert_to_scalar(DEFAULT_THICKNESS / 2),
        )
        return self.end_marker

    def get_markers(self) -> tuple[Marker, Marker | None]:
        return self.start_marker, self.end_marker

    def get_labels(self) -> list[Label]:
        return [
            label
            for marker in self.get_markers()
            if marker
            for label in marker.get_labels()
        ]

    def get_straight_line(self) -> StraightLine:
        return self._straight_line

    @property
    def length(self) -> Scalar:
        return self._straight_line.length

    @length.setter
    def length(self, value: Scalar) -> None:
        self._straight_line.length = value

    @property
    def color(self) -> str:
        return self._straight_line.color

    @color.setter
    def color(self, value: str):
        self._straight_line.color = value
        self.start_marker.color = value
        if self.end_marker:
            self.end_marker.color = value

    @property
    def thickness(self) -> Scalar:
        return self._straight_line.thickness

    @thickness.setter
    def thickness(self, value: Scalar):
        self._straight_line.thickness = value


class SegmentedLine:
    def __init__(
        self,
        *,
        type: LineOrientation,
    ) -> None:
        super().__init__()
        self._type = type
        self._line_segments: list[LineSegment] = []

    def add_line_segment(self, line_segment: LineSegment):
        if line_segment.type != self._type:
            raise TypeError("line orientation mismatch")
        self._line_segments.append(line_segment)
        return line_segment

    def get_line_segments(self) -> list[LineSegment]:
        return self._line_segments

    def get_length(self) -> Scalar:
        return sum([sl.length for sl in self.get_line_segments()])
