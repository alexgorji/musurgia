from unittest import TestCase


from musurgia.graphics.drawobject import (
    Position,
    StraightLineDrawObject,
)
from musurgia.graphics.line_segment import (
    Label,
    LineSegment,
    Marker,
    MarkerOptions,
)
from musurgia.graphics.models import LineOrientation


class MarkerTestCase(TestCase):
    def test_type(self):
        m = Marker(type=LineOrientation.VERTICAL, options={"length": 10})
        assert m.get_type() == LineOrientation.VERTICAL.value
        assert m.get_length() == 10

    def test_labels(self):
        labels = [Label(text="First Layer"), Label(text="Second Layer", offset=10)]
        m = Marker(
            type=LineOrientation.VERTICAL,
            options={
                "length": 10,
                "labels": labels,
            },
        )
        assert len(m.get_labels()) == 2
        assert set(
            [(label.text, label.get_offset()) for label in m.get_labels()]
        ) == set([(label.text, label.get_offset()) for label in labels])
        assert m.size.height == 10 + 10


class HorizontalLineSegmentTestCase(TestCase):
    def test_get_draw_objects(self):
        hsl = LineSegment(
            type=LineOrientation.HORIZONTAL, length=25, color="blue", thickness=1
        )
        assert len(hsl.get_positioned_draw_objects()) == 3
        assert len(hsl.get_positioned_draw_objects(recursive=True)) == 3

    def test_components(self):
        hsl = LineSegment(
            type=LineOrientation.HORIZONTAL,
            length=15,
        )

        start_marker, end_marker = hsl.get_markers()
        assert isinstance(start_marker, Marker)
        assert isinstance(end_marker, Marker)
        assert start_marker.get_type() == end_marker.get_type() == "vertical"
        assert start_marker.get_length() == MarkerOptions.length
        assert end_marker.get_length() == MarkerOptions.length
        straight_line = hsl.get_straight_line()
        assert isinstance(straight_line, StraightLineDrawObject)
        assert straight_line.type.value == "horizontal"
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

    def test_no_end_marker_components(self):
        hsl = LineSegment(
            type=LineOrientation.HORIZONTAL, length=15, no_end_marker=True
        )

        start_marker, end_marker = hsl.get_markers()
        assert end_marker is None
        assert isinstance(start_marker, Marker)
        assert start_marker.get_type() == "vertical"
        assert start_marker.get_length() == MarkerOptions.length
        straight_line = hsl.get_straight_line()
        assert isinstance(straight_line, StraightLineDrawObject)
        assert straight_line.type.value == "horizontal"
        assert straight_line.get_length() == 15
        assert {do[1] for do in hsl.get_positioned_draw_objects()} == {
            start_marker,
            straight_line,
        }

        for p, o in hsl.get_positioned_draw_objects():
            if o == start_marker:
                assert p == Position(0, 0)
            elif o == straight_line:
                assert p == Position(0, 3)

    def test_set_color(self):
        hsl = LineSegment(
            type=LineOrientation.HORIZONTAL,
            length=15,
            color="blue",
        )
        assert {
            o.color for _, o in hsl.get_positioned_draw_objects(recursive=True)
        } == {"blue"}

    def test_set_thickness(self):
        hsl = LineSegment(
            type=LineOrientation.HORIZONTAL,
            length=25,
            thickness=1,
            options={"straight_line": {"thickness": 2}},
        )
        for _, o in hsl.get_positioned_draw_objects(recursive=True):
            if isinstance(o, StraightLineDrawObject):
                if o.type.value == "horizontal":
                    assert o.thickness == 2
                else:
                    assert o.thickness == 1

    def test_different_marker_sizes(self):
        hsl = LineSegment(
            type=LineOrientation.HORIZONTAL,
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

        hsl = LineSegment(
            type=LineOrientation.HORIZONTAL,
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

    def test_component_getters(self):
        hsl = LineSegment(type=LineOrientation.HORIZONTAL, length=15)
        assert hsl.get_straight_line(positioned=True)[0] == Position(0, 3)
        straight_line = hsl.get_straight_line(positioned=True)[1]
        assert isinstance(straight_line, StraightLineDrawObject)
        assert straight_line == hsl.get_straight_line(positioned=False)

        positioned_start, positioned_end = hsl.get_markers(positioned=True)
        start, end = hsl.get_markers(positioned=False)

        assert positioned_start[1] == start
        assert positioned_start[0] == Position(0, 0)
        assert start.get_length() == 6

        if positioned_end and end:
            assert positioned_end[1] == end
            assert positioned_end[0] == Position(15, 0)
            assert end.get_length() == 6

    def test_add_labels(self):
        labels = [
            Label(text="first layer", offset=20),
            Label(text="Second layer", offset=10),
        ]

        hsl = LineSegment(
            type=LineOrientation.HORIZONTAL,
            length=10,
            options={"start_marker": {"labels": labels, "length": 30}},
        )
        start, _ = hsl.get_markers()

        assert len(start.get_labels()) == 2
        assert set(
            [(label.text, label.get_offset()) for label in start.get_labels()]
        ) == set([(label.text, label.get_offset()) for label in labels])
        assert start.size.height == 30 + 20


class VerticalLineSegmentTestCase(TestCase):
    def test_get_draw_objects(self):
        vsl = LineSegment(
            type=LineOrientation.VERTICAL, length=25, color="blue", thickness=1
        )
        assert len(vsl.get_positioned_draw_objects()) == 3
        assert len(vsl.get_positioned_draw_objects(recursive=True)) == 3

    def test_components(self):
        vsl = LineSegment(
            type=LineOrientation.VERTICAL,
            length=15,
        )

        start_marker, end_marker = vsl.get_markers()
        assert isinstance(start_marker, Marker)
        assert isinstance(end_marker, Marker)
        assert start_marker.get_type() == end_marker.get_type() == "horizontal"
        assert start_marker.get_length() == MarkerOptions.length
        assert end_marker.get_length() == MarkerOptions.length
        straight_line = vsl.get_straight_line()
        assert isinstance(straight_line, StraightLineDrawObject)
        assert straight_line.type.value == "vertical"
        assert straight_line.get_length() == 15
        assert {do[1] for do in vsl.get_positioned_draw_objects()} == {
            start_marker,
            end_marker,
            straight_line,
        }

        for p, o in vsl.get_positioned_draw_objects():
            if o == start_marker:
                assert p == Position(0, 0)
            elif o == end_marker:
                assert p == Position(0, 15)
            elif o == straight_line:
                assert p == Position(3, 0)

    def test_set_thickness(self):
        vsl = LineSegment(
            type=LineOrientation.VERTICAL,
            length=25,
            thickness=1,
            options={"straight_line": {"thickness": 2}},
        )
        for _, o in vsl.get_positioned_draw_objects(recursive=True):
            if isinstance(o, StraightLineDrawObject):
                if o.type.value == "vertical":
                    assert o.thickness == 2
                else:
                    assert o.thickness == 1

    def test_different_marker_sizes(self):
        vsl = LineSegment(
            type=LineOrientation.VERTICAL,
            length=10,
            options={"start_marker": {"length": 10}, "end_marker": {"length": 5}},
        )

        positioned_start_marker = next(
            (p, o)
            for (p, o) in vsl.get_positioned_draw_objects()
            if o == vsl._start_marker
        )

        positioned_end_marker = next(
            (p, o)
            for (p, o) in vsl.get_positioned_draw_objects()
            if o == vsl._end_marker
        )

        assert positioned_start_marker[0] == Position(0, 0)

        assert positioned_end_marker[0] == Position(2.5, 10)

        vsl = LineSegment(
            type=LineOrientation.VERTICAL,
            length=10,
            options={"start_marker": {"length": 5}, "end_marker": {"length": 10}},
        )

        positioned_start_marker = next(
            (p, o)
            for (p, o) in vsl.get_positioned_draw_objects()
            if o == vsl._start_marker
        )

        positioned_end_marker = next(
            (p, o)
            for (p, o) in vsl.get_positioned_draw_objects()
            if o == vsl._end_marker
        )

        assert positioned_start_marker[0] == Position(2.5, 0)

        assert positioned_end_marker[0] == Position(0, 10)

    def test_component_getters(self):
        vsl = LineSegment(type=LineOrientation.VERTICAL, length=15)
        assert vsl.get_straight_line(positioned=True)[0] == Position(3, 0)
        straight_line = vsl.get_straight_line(positioned=True)[1]
        assert isinstance(straight_line, StraightLineDrawObject)
        assert straight_line == vsl.get_straight_line(positioned=False)

        positioned_start, positioned_end = vsl.get_markers(positioned=True)
        start, end = vsl.get_markers(positioned=False)

        assert positioned_start[1] == start
        assert positioned_start[0] == Position(0, 0)
        assert start.get_length() == 6

        if positioned_end and end:
            assert positioned_end[1] == end
            assert positioned_end[0] == Position(0, 15)
            assert end.get_length() == 6
