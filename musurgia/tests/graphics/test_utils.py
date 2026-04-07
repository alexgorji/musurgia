from unittest import TestCase

from musurgia.graphics.geometry import Position
from musurgia.graphics.geometry import LineOrientation
from musurgia.graphics.segmented_line import LineSegment, SegmentedLine
from musurgia.graphics.util import (
    override_options_mappings,
    toggle_line_orientation,
    toggle_position,
)


class Toggles(TestCase):
    def test_toggle_line_orientations(self):
        o = LineOrientation.HORIZONTAL
        toggled = toggle_line_orientation(o)
        assert toggled == LineOrientation.VERTICAL
        assert toggle_line_orientation(toggled) == o

    def test_toggle_postions(self):
        p = Position(100, 200)
        toggled = toggle_position(p)
        assert toggled == Position(200, 100)
        assert toggle_position(toggled) == p


class OverrideOptionsMappings(TestCase):
    def test_override_simple(self):
        options = {"start_marker": {"length": 10, "color": "blue"}}
        override = {
            "start_marker": {"length": 20},
            "end_marker": {"length": 30, "color": "red"},
        }
        assert override_options_mappings(options, override) == {
            "start_marker": {"length": 20, "color": "blue"},
            "end_marker": {"length": 30, "color": "red"},
        }


def check_straight_line_alignment(segmented_line: SegmentedLine):
    positioned_line_segments = segmented_line.get_line_segments(positioned=True)
    first_positioned_line_segment = positioned_line_segments[0]

    if segmented_line.type.value == "horizontal":
        first_straight_line_y = (
            first_positioned_line_segment[1].get_straight_line(positioned=True)[0].y
            + first_positioned_line_segment[0].y
        )
        for ls in positioned_line_segments[1:]:
            assert (
                ls[1].get_straight_line(positioned=True)[0].y + ls[0].y
                == first_straight_line_y
            )
    else:
        first_straight_line_x = (
            first_positioned_line_segment[1].get_straight_line(positioned=True)[0].x
            + first_positioned_line_segment[0].x
        )
        for ls in positioned_line_segments[1:]:
            assert (
                ls[1].get_straight_line(positioned=True)[0].x + ls[0].x
                == first_straight_line_x
            )


def check_centered_markers(line_segment: LineSegment):
    straight_line_position = line_segment.get_straight_line(positioned=True)[0]
    positioned_start_marker, _ = line_segment.get_markers(positioned=True)
    positioned_start_marker_line = positioned_start_marker[1].get_line(positioned=True)

    if line_segment.type.value == "horizontal":
        assert (
            positioned_start_marker[0].y
            + positioned_start_marker_line[0].y
            + positioned_start_marker[1].get_length() / 2
            == straight_line_position.y
        )
    elif line_segment.type.value == "vertical":
        assert (
            positioned_start_marker[0].x
            + positioned_start_marker_line[0].x
            + positioned_start_marker[1].get_length() / 2
            == straight_line_position.x
        )
    else:
        raise TypeError()
    return True


def check_all_straight_lines_centered(segmented_line: SegmentedLine):
    for ls in segmented_line.get_line_segments():
        assert check_centered_markers(ls)
    return True
