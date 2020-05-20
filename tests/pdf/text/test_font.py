from musurgia.pdf.font import Font
from musurgia.unittest import TestCase


class TestFont(TestCase):
    def setUp(self) -> None:
        self.font = Font()

    def test_height(self):
        actual = self.font.get_text_pixel_height()
    #     expected = 10
    #     self.assertEqual(expected, actual)