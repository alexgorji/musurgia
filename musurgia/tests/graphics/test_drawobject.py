from unittest import TestCase
from musurgia.graphics.drawobject import (
    DrawObjectBox,
    HorizontalLineDrawObject,
    VerticalLineDrawObject,
)


class LineDrawObjectTestCase(TestCase):

    def test_horizontal_line(self):
        hl = HorizontalLineDrawObject(start={"x": 20, "y": 40}, length=10)
        assert hl.end == {"x": 30, "y": 40}

    def test_vertical_line(self):
        hl = VerticalLineDrawObject(start={"x": 20, "y": 30}, length=10)
        assert hl.end == {"x": 20, "y": 40}


class DrawObjectBoxTestCase(TestCase):
    def test_get_box_size(self):
        hl = HorizontalLineDrawObject(
            start={"x": 20, "y": 40}, length=20, stroke_width=1
        )
        marker_1 = VerticalLineDrawObject(
            start={"x": 20, "y": 37}, length=6, stroke_width=1
        )
        marker_2 = VerticalLineDrawObject(
            start={"x": 40, "y": 37}, length=6, stroke_width=1
        )
        box = DrawObjectBox()
        box.add_draw_object(hl).add_draw_object(marker_1).add_draw_object(marker_2)
        assert box.size == {"width": 41, "height": 43}
