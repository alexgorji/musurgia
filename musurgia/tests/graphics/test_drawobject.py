from unittest import TestCase
from musurgia.graphics.drawobject import (
    HorizontalLineDrawObject,
    LineDrawObject,
    TextDrawObject,
    VerticalLineDrawObject,
)


class TextDrawObjectTestCase(TestCase):
    def test_default_values(self):
        # text default value needed
        with self.assertRaises(TypeError):
            TextDrawObject()
        text = TextDrawObject("some text")
        assert text.text == "some text"
        assert text.layout.get_relative_position() == {"relative_x": 0, "relative_y": 0}
        assert text.layout.get_absolute_position() == {"x": 0, "y": 0}
        assert text.font_size == 12
        assert text.font_family == "Helvetica"
        assert text.color == "black"


class LineDrawObjectTestCase(TestCase):
    def test_default_start(self):
        l = LineDrawObject(end={"x": 10, "y": 20})
        assert l.start == {"x": 0, "y": 0}

    def test_horizontal_line(self):
        hl = HorizontalLineDrawObject(start={"x": 20, "y": 40}, length=10)
        assert hl.end == {"x": 30, "y": 40}

    def test_vertical_line(self):
        hl = VerticalLineDrawObject(start={"x": 20, "y": 30}, length=10)
        assert hl.end == {"x": 20, "y": 40}
