from musurgia.pdf.font import Font, FontError
from musurgia.tests.unitintegrationtests._test_utils import TestCase


class TestFont(TestCase):
    def setUp(self) -> None:
        self.font = Font()

    def test_load_afm(self):
        afm = self.font._afm
        actual = afm.get_familyname()
        expected = self.font.family
        self.assertEqual(expected, actual)

    def test_text_pixel_height(self):
        self.font.size = 12
        actual = round(self.font.get_text_pixel_height('This One'), 3)
        expected = 8.1
        self.assertEqual(expected, actual)

    def test_text_pixel_width(self):
        self.font.size = 11
        actual = round(self.font.get_text_pixel_width('This One'), 3)
        expected = 52.8
        self.assertEqual(expected, actual)

    def test_errors(self):
        with self.assertRaises(FontError):
            self.font.family = 'Bla'

        with self.assertRaises(FontError):
            self.font.style = 'Bla'

        with self.assertRaises(FontError):
            self.font.weight = 'Bla'
