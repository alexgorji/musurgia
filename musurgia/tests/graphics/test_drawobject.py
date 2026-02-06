from unittest import TestCase
from musurgia.graphics.drawobject import TextDrawObject


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
