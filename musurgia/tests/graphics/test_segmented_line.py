from unittest import TestCase

from musurgia.graphics.drawobject import HorizontalLineDrawObject, Position
from musurgia.graphics.segmented_line import (
    HorizontalSegmentedLine,
    Marker,
    MarkerOptions,
    MarkerType,
)


class MarkerTestCase(TestCase):
    def test_marker_type(self):
        m = Marker(MarkerType.VERTICAL, {"length": 10})
        assert m.get_type() == MarkerType.VERTICAL.value
        assert m.get_length() == 10


class SegmentedLineTestCase(TestCase):
    def test_horizontal_segmented_line_container_components(self):
        hsl = HorizontalSegmentedLine(
            length=15,
        )
        start_marker, end_marker = hsl.get_markers()
        assert isinstance(start_marker, Marker)
        assert isinstance(end_marker, Marker)
        assert start_marker.get_type() == end_marker.get_type() == "vertical"
        assert start_marker.get_length() == MarkerOptions.length
        assert end_marker.get_length() == MarkerOptions.length
        straight_line = hsl.get_straight_line()
        assert isinstance(straight_line, HorizontalLineDrawObject)
        assert straight_line.get_length() == 15
        assert {do[1] for do in hsl.get_draw_objects()} == {
            start_marker,
            end_marker,
            straight_line,
        }

        for p, o in hsl.get_draw_objects():
            if o == start_marker:
                assert p == Position(0, 0)
            elif o == end_marker:
                assert p == Position(15, 0)
            elif o == straight_line:
                assert p == Position(0, 3)
