from unittest import TestCase


from musurgia.graphics.drawobject import (
    HorizontalLineDrawObject,
    Position,
    VerticalLineDrawObject,
)
from musurgia.graphics.line_segment import (
    HorizontalLineSegment,
    Marker,
    MarkerOptions,
    MarkerType,
)


class MarkerTestCase(TestCase):
    def test_type(self):
        m = Marker(type=MarkerType.VERTICAL, options={"length": 10})
        assert m.get_type() == MarkerType.VERTICAL.value
        assert m.get_length() == 10


class HorizontalLineSegmentTestCase(TestCase):
    def test_get_draw_objects(self):
        hsl = HorizontalLineSegment(length=25, color="blue", thickness=1)
        assert len(hsl.get_positioned_draw_objects()) == 3
        assert len(hsl.get_positioned_draw_objects(recursive=True)) == 3

    def test_components(self):
        hsl = HorizontalLineSegment(
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
        assert {do[1] for do in hsl.get_positioned_draw_objects()} == {
            start_marker,
            end_marker,
            straight_line,
        }

        for p, o in hsl.get_positioned_draw_objects():
            if o == start_marker:
                assert p == Position(0, 0)
            elif o == end_marker:
                assert p == Position(15, 0)
            elif o == straight_line:
                assert p == Position(0, 3)

    def test_set_color(self):
        hsl = HorizontalLineSegment(
            length=15,
            color="blue",
        )
        assert {
            o.color for _, o in hsl.get_positioned_draw_objects(recursive=True)
        } == {"blue"}

    def test_set_thickness(self):
        hsl = HorizontalLineSegment(
            length=25, thickness=1, options={"straight_line": {"thickness": 2}}
        )
        for _, o in hsl.get_positioned_draw_objects(recursive=True):
            if isinstance(o, VerticalLineDrawObject):
                assert o.thickness == 1
            if isinstance(o, HorizontalLineDrawObject):
                assert o.thickness == 2

    def test_different_marker_sizes(self):
        hsl = HorizontalLineSegment(
            length=10,
            options={"start_marker": {"length": 10}, "end_marker": {"length": 5}},
        )

        positioned_start_marker = next(
            (p, o)
            for (p, o) in hsl.get_positioned_draw_objects()
            if o == hsl._start_marker
        )

        positioned_end_marker = next(
            (p, o)
            for (p, o) in hsl.get_positioned_draw_objects()
            if o == hsl._end_marker
        )

        assert positioned_start_marker[0] == Position(0, 0)

        assert positioned_end_marker[0] == Position(10, 2.5)

        hsl = HorizontalLineSegment(
            length=10,
            options={"start_marker": {"length": 5}, "end_marker": {"length": 10}},
        )

        positioned_start_marker = next(
            (p, o)
            for (p, o) in hsl.get_positioned_draw_objects()
            if o == hsl._start_marker
        )

        positioned_end_marker = next(
            (p, o)
            for (p, o) in hsl.get_positioned_draw_objects()
            if o == hsl._end_marker
        )

        assert positioned_start_marker[0] == Position(0, 2.5)

        assert positioned_end_marker[0] == Position(10, 0)
