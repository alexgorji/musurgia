from typing import List, cast
from unittest import TestCase


from musurgia.graphics.drawobject import LineDrawObject, TextDrawObject
from musurgia.graphics.line_segment import HorizontalLineSegment
from musurgia.graphics.ruler import HorizontalRuler, RulerUnit


class RulerUnitTestCase(TestCase):

    def test_components(self):
        ru = RulerUnit(
            length=20, division=5, large_markers_length=5, small_markers_length=2.5
        )
        positioned_dos = ru.get_positioned_draw_objects()
        dos = [o for _, o in positioned_dos]
        pos = [p for p, _ in positioned_dos]
        assert len(dos) == 5
        for o in dos:
            assert isinstance(o, HorizontalLineSegment)

        assert [cast(HorizontalLineSegment, o)._length for o in dos] == [4, 4, 4, 4, 4]
        assert [p.x for p in pos] == [0, 4, 8, 12, 16]

    def test_markers(self):
        ru = RulerUnit(
            length=20, division=5, large_markers_length=5, small_markers_length=2.5
        )
        dos = cast(List[HorizontalLineSegment], ru.get_draw_objects())

        assert [o._start_marker.show for o in dos] == [
            True,
            True,
            True,
            True,
            True,
        ]
        assert [o._end_marker.show for o in dos] == [
            False,
            False,
            False,
            False,
            False,
        ]

        assert [o._start_marker.get_length() for o in dos] == [
            5,
            2.5,
            2.5,
            2.5,
            2.5,
        ]

        assert [o._end_marker.get_length() for o in dos] == [
            2.5,
            2.5,
            2.5,
            2.5,
            5,
        ]

    def test_color(self):
        ru = RulerUnit(
            length=20,
            division=5,
            large_markers_length=5,
            small_markers_length=2.5,
            color="blue",
        )
        dos = cast(
            List[LineDrawObject | TextDrawObject], ru.get_draw_objects(recursive=True)
        )
        for d in dos:
            assert d.color == "blue"

    def test_thickness(self):
        ru = RulerUnit(
            length=20,
            division=5,
            large_markers_length=5,
            small_markers_length=2.5,
            thickness=1.0,
        )

        dos = cast(List[HorizontalLineSegment], ru.get_draw_objects())
        for d in dos:
            assert d._straight_line.thickness == 1.0

        assert [o._start_marker.get_thickness() for o in dos] == [
            1.0,
            0.5,
            0.5,
            0.5,
            0.5,
        ]

        assert [o._end_marker.get_thickness() for o in dos] == [
            0.5,
            0.5,
            0.5,
            0.5,
            1.0,
        ]


class HorizontalRulerTests(TestCase):
    def test_ruler_units(self):
        hr = HorizontalRuler(length=60)
        assert len(hr._ruler_units) == 6
        for ru in hr._ruler_units:
            assert isinstance(ru, RulerUnit)
        ru = hr._ruler_units[0]
        assert ru._length == 10
        assert ru._division == 10

    def test_show_numbers(self):
        hr = HorizontalRuler(length=60)
