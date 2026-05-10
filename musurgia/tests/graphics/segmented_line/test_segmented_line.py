from pathlib import Path

import pytest


from musurgia.graphics.geometry import LineOrientation, Position

from musurgia.graphics.segmented_line import (
    DEFAULT_COLOR,
    DEFAULT_THICKNESS,
    Label,
    LineSegment,
    SegmentedLine,
)
from musurgia.graphics.svg.paginator import SVGPage
from musurgia.tests.helpers.svg import SVGTestCase

path = Path(__file__)
# pytestmark = pytest.mark.only


def test_create_line_segment():
    ls = LineSegment(type=LineOrientation.HORIZONTAL, length=20)
    assert ls.end_marker is None
    em = ls.add_end_maker()
    sm = ls.start_marker
    assert ls.length == 20
    assert ls.color == sm.options.color == em.options.color == DEFAULT_COLOR
    assert ls.thickness == DEFAULT_THICKNESS
    assert sm.options.thickness == em.options.thickness == DEFAULT_THICKNESS
    ls.build()
    assert ls.straight_line in ls.get_draw_objects()
    assert sm in ls.get_draw_objects()
    assert em in ls.get_draw_objects()


def test_add_lable_to_marker():
    ls = LineSegment(type=LineOrientation.HORIZONTAL, length=20)
    l1 = ls.start_marker.add_label(Label(text="first"))
    l2 = ls.start_marker.add_label(Label(text="second", offset=Position(2, 10)))

    ls.build()
    assert l1 in ls.start_marker.get_draw_objects()
    assert l2 in ls.start_marker.get_draw_objects()


def test_segmented_line_create():
    ls1 = LineSegment(type=LineOrientation.HORIZONTAL, length=20)
    sl = SegmentedLine(
        type=LineOrientation.HORIZONTAL,
        line_segments=[ls1],
    )
    assert ls1 in sl.get_line_segments()
    ls2 = LineSegment(type=LineOrientation.HORIZONTAL, length=10)
    sl.add_line_segment(ls2)
    assert len(sl.get_line_segments()) == 2
    assert sl.get_length() == 30
    sl.build()
    assert ls1 in sl.get_draw_objects()
    assert ls1 in sl.get_draw_objects()


def test_segmented_line_segmented_lines_factory():
    ls1 = LineSegment(type=LineOrientation.HORIZONTAL, length=20)
    sl = SegmentedLine(
        type=LineOrientation.HORIZONTAL,
        line_segments=[ls1],
    )
    new_lss = sl.add_line_segments(lengths=[5, 10, 15], color="red")
    assert len(sl.get_line_segments()) == 4
    for ls in new_lss:
        assert ls in sl.get_line_segments()
        assert ls.color == "red"
    assert ls1.color == DEFAULT_COLOR


@pytest.mark.nonci
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

        self.compare_page(
            page, "line_segmented_horizontal", path, width=210 * 2, height=297 * 2
        )

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

        self.compare_page(
            page, "line_segmented_vertical", path, width=210 * 2, height=297 * 2
        )


@pytest.mark.nonci
class SegmentedLineDraw(SVGTestCase):
    def test_draw_segment_line_horizontal(self):
        sl = SegmentedLine(type=LineOrientation.HORIZONTAL)
        lss = sl.add_line_segments(lengths=[5, 10, 15])
        texts = ["one", "two", "tree"]
        for i, ls in enumerate(lss):
            ls.start_marker.length += i * 4
            ls.start_marker.add_label(
                Label(text=texts[i], offset=Position(i * 2, i * 3))
            )
        sl.box.show = True
        sl.build()
        page = SVGPage()
        page.add_grid()
        page.add_background("white")
        page.add_draw_object(Position(10, 10), sl)

        self.compare_page(page, "horizontal", path, width=210 * 2, height=297 * 2)

    def test_draw_segment_line_vertical(self):
        sl = SegmentedLine(type=LineOrientation.VERTICAL)
        lss = sl.add_line_segments(lengths=[5, 10, 15])
        texts = ["one", "two", "tree"]
        for i, ls in enumerate(lss):
            ls.start_marker.length += i * 4
            ls.start_marker.add_label(
                Label(text=texts[i], offset=Position(i * 3, i * 2))
            )
        sl.box.show = True
        sl.build()
        page = SVGPage()
        page.add_grid()
        page.add_background("white")
        page.add_draw_object(Position(10, 10), sl)

        self.compare_page(page, "vertical", path, width=210 * 2, height=297 * 2)
