from pathlib import Path

from musurgia.pdf.pdf import Pdf
from musurgia.pdf.text import Text
from musurgia.unittest import TestCase

path = Path(__file__)


class TestText(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_draw(self):
        t = Text('fox is going to be dead.')
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            t.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_draw_with_top_margin(self):
        t = Text('fox is going to be dead.')
        t.top_margin = 2
        with self.file_path(path, 'draw_with_top_margin', 'pdf') as pdf_path:
            t.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_get_height(self):
        t = Text('fox is going to be dead.')
        t.font_size = 14
        t.top_margin = 3
        expected = 7.682066666666666
        actual = t.get_height()
        self.assertEqual(expected, actual)
