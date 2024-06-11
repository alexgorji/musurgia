from pathlib import Path

from musurgia.pdf.line import VerticalLineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestVerticalLineSegment(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.vls = VerticalLineSegment(length=10)

    def test_get_relative_x2(self):
        assert self.vls.get_relative_x2() == self.vls.get_width()

    def test_start_mark_line_relative_x(self):
        assert self.vls.start_mark_line.relative_x == 0

    def test_start_mark_line_relative_y(self):
        actual = self.vls.start_mark_line.relative_y
        expected = self.vls.relative_y
        self.assertEqual(expected, actual)

    def test_end_mark_line_relative_y(self):
        assert self.vls.end_mark_line.relative_y == self.vls.relative_y + self.vls.length

    def test_end_mark_line_relative_x(self):
        assert self.vls.end_mark_line.relative_x == 0

    def test_start_mark_line_top_margin(self):
        actual = self.vls.start_mark_line.top_margin
        expected = 0
        self.assertEqual(expected, actual)

    def test_get_width(self):
        actual = self.vls.get_width()
        expected = 3
        self.assertEqual(expected, actual)

    def test_draw(self):
        with self.file_path(parent_path=path, name='draw', extension='pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.vls.end_mark_line.show = True
            self.vls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
