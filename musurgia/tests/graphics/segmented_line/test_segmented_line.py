from pathlib import Path

import pytest

from musurgia.graphics.geometry import Coordinates, LineOrientation, Position, Size

from musurgia.graphics.segmented_line import (
    DEFAULT_COLOR,
    DEFAULT_THICKNESS,
    Label,
    LineSegment,
    StraightLine,
)
from musurgia.graphics.svg.paginator import SVGPage
from musurgia.graphics.util import convert_to_scalar
from musurgia.tests.helpers.svg import SVGTestCase

path = Path(__file__)
# pytestmark = pytest.mark.only


def test_straight_line_get_bounding_box_coordinates():
    sl = StraightLine(type=LineOrientation.HORIZONTAL, length=10)
    assert sl.size == Size(10, 2)
    assert sl.get_bounding_box_coordinates() == Coordinates(
        Position(0, 0), Position(10, 0), Position(10, 2), Position(0, 2)
    )


def test_create_line_segment():
    ls = LineSegment(type=LineOrientation.HORIZONTAL, length=20)
    assert ls.end_marker is None
    em = ls.add_end_maker()
    sm = ls.start_marker
    assert ls.length == 20
    assert ls.color == sm.color == em.color == DEFAULT_COLOR
    assert ls.thickness == DEFAULT_THICKNESS
    assert sm.thickness == em.thickness == convert_to_scalar(DEFAULT_THICKNESS / 2)
    ls.build()
    assert ls.get_straight_line() in ls.get_draw_objects()
    assert sm in ls.get_draw_objects()
    assert em in ls.get_draw_objects()


def test_add_lable_to_marker():
    ls = LineSegment(type=LineOrientation.HORIZONTAL, length=20)
    l1 = ls.start_marker.add_label(Label(text="first"))
    l2 = ls.start_marker.add_label(Label(text="second", offset=Position(2, 10)))

    ls.build()
    assert l1 in ls.start_marker.get_draw_objects()
    assert l2 in ls.start_marker.get_draw_objects()


class LineSegmentDraw(SVGTestCase):
    def test_draw_line_segment_horizontal(self):
        ls = LineSegment(type=LineOrientation.HORIZONTAL, length=20)
        ls.start_marker.add_label(Label(text="first"))
        ls.start_marker.add_label(Label(text="second", offset=Position(2, 10)))
        ls.box.show = True
        ls.build()
        page = SVGPage()
        page.add_grid()
        page.add_background("white")
        page.add_draw_object(Position(10, 10), ls)

        self.compare_page(page, "horizontal", path, width=210 * 2, height=297 * 2)

    def test_draw_line_segment_vertical(self):
        ls = LineSegment(type=LineOrientation.VERTICAL, length=20)
        ls.start_marker.add_label(Label(text="first"))
        ls.start_marker.add_label(Label(text="second", offset=Position(10, 2)))
        ls.box.show = True
        ls.build()
        page = SVGPage()
        page.add_grid()
        page.add_background("white")
        page.add_draw_object(Position(10, 10), ls)

        self.compare_page(page, "vertical", path, width=210 * 2, height=297 * 2)
