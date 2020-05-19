from pathlib import Path

from musurgia.pdf.line import LineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.unittest import TestCase

path = Path(__file__)


class TestLineSegment(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.ls = LineSegment(mode='horizontal', length=10)

    def test_get_relative_x2(self):
        actual = self.ls.get_relative_x2()
        expected = self.ls.length
        self.assertEqual(expected, actual)

    def test_start_mark_line_relative_x(self):
        actual = self.ls.start_mark_line.relative_x
        expected = self.ls.relative_x
        self.assertEqual(expected, actual)

    def test_start_mark_line_relative_y(self):
        actual = self.ls.start_mark_line.relative_y
        expected = self.ls.relative_y
        self.assertEqual(expected, actual)

    def test_end_mark_line_relative_x(self):
        actual = self.ls.end_mark_line.relative_x
        expected = self.ls.relative_x + self.ls.length
        self.assertEqual(expected, actual)

    def test_end_mark_line_relative_y(self):
        actual = self.ls.end_mark_line.relative_y
        expected = self.ls.relative_y
        self.assertEqual(expected, actual)

    def test_draw(self):
        with self.file_path(parent_path=path, name='draw', extension='pdf') as pdf_path:
            self.pdf.translate(self.pdf.l_margin, self.pdf.t_margin)
            self.ls.end_mark_line.show = True
            with self.pdf.saved_state():
                self.ls.draw(self.pdf)
            self.pdf.write(pdf_path)
