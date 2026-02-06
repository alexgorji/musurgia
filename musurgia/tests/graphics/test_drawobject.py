from unittest import TestCase
from musurgia.graphics.drawobject import (
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
