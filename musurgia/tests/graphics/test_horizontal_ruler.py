from typing import List, cast
from unittest import TestCase


from musurgia.graphics.drawobject import LineDrawObject, TextDrawObject
from musurgia.graphics.line_segment import HorizontalLineSegment, Marker
from musurgia.graphics.ruler import (
    HorizontalRuler,
    RulerUnit,
)


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

    def test_get_positioned_ruler_units(self):
        hr = HorizontalRuler(length=30, unit_division=3)
        rus = hr.get_positioned_ruler_units()
        assert len(rus) == 3
        assert [p.x for p, _ in rus] == [0, 10, 20]
        assert [o for _, o in rus] == hr._ruler_units

    def test_get_position_markers(self):
        hr = HorizontalRuler(length=20, unit_division=3)
        markers = hr.get_positioned_markers()
        assert len(markers) == 6
        assert [round(p.x, 3) for p, _ in markers] == [
            0,
            3.333,
            6.667,
            10,
            13.333,
            16.667,
        ]
        for _, m in markers:
            assert isinstance(m, Marker)


class HorizontalRulerTestsLabels(TestCase):
    hr1 = HorizontalRuler(length=60)
    hr2 = HorizontalRuler(
        length=120, unit_length=20, unit_division=5, labels_interval=3
    )

    def test_get_division_size(self):
        assert self.hr1._get_division_size() == 1
        assert self.hr2._get_division_size() == 4

    def test_build_labels(self):
        labels = self.hr1.get_positioned_labels()
        assert len(labels) == 6
        for i, (_, label) in enumerate(labels):
            assert isinstance(label, TextDrawObject)
            assert label.text == str(i)

        labels = self.hr2.get_positioned_labels()

        assert len(labels) == 2
        for i, (_, label) in enumerate(labels):
            assert isinstance(label, TextDrawObject)
            assert label.text == str(i * 3)
