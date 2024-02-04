from musurgia.pdf.font import Font, FontError
from musurgia.tests.unitintegrationtests.test_utils import TestCase


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
        actual = self.font.get_text_pixel_height('This One')
        expected = 8.844
        self.assertEqual(expected, actual)

    def test_text_pixel_width(self):
        self.font.size = 11
        actual = self.font.get_text_pixel_width('This One')
        expected = 44.627
        self.assertEqual(expected, actual)

    def test_errors(self):
        with self.assertRaises(FontError):
            self.font.family = 'Bla'

        with self.assertRaises(FontError):
            self.font.style = 'Bla'

        with self.assertRaises(FontError):
            self.font.weight = 'Bla'
