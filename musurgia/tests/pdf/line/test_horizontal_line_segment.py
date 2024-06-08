from pathlib import Path

from musurgia.pdf.line import HorizontalLineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestHorizontalLineSegment(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.hls = HorizontalLineSegment(length=10)

    def test_get_relative_x2(self):
        actual = self.hls.get_relative_x2()
        expected = self.hls.length
        self.assertEqual(expected, actual)

    def test_start_mark_line_relative_x(self):
        actual = self.hls.start_mark_line.relative_x
        expected = self.hls.relative_x
        self.assertEqual(expected, actual)

    def test_start_mark_line_relative_y(self):
        actual = self.hls.start_mark_line.relative_y
        expected = -1.5
        self.assertEqual(expected, actual)

    def test_end_mark_line_relative_x(self):
        actual = self.hls.end_mark_line.relative_x
        expected = self.hls.relative_x + self.hls.length
        self.assertEqual(expected, actual)

    def test_end_mark_line_relative_y(self):
        actual = self.hls.end_mark_line.relative_y
        expected = -1.5
        self.assertEqual(expected, actual)

    def test_straight_line_top_margin(self):
        actual = self.hls.straight_line.top_margin
        expected = 0
        self.assertEqual(expected, actual)

    def test_start_mark_line_top_margin(self):
        actual = self.hls.start_mark_line.top_margin
        expected = 0
        self.assertEqual(expected, actual)

    def test_get_height(self):
        actual = self.hls.get_height()
        expected = 3
        self.assertEqual(expected, actual)

    def test_set_and_get_length(self):
        assert self.hls.length == 10
        self.hls.length = 20
        assert self.hls.length == 20

    def test_draw(self):
        with self.file_path(parent_path=path, name='draw', extension='pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(10, 10)
            self.hls.end_mark_line.show = True
            self.hls.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_draw_list(self):
        segments = [HorizontalLineSegment(length) for length in range(10, 30, 5)]
        segments[-1].end_mark_line.show = True
        with self.file_path(parent_path=path, name='draw_list', extension='pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(10, 10)
            for segment in segments:
                segment.draw(self.pdf)
                self.pdf.translate(segment.get_width(), 0)

            self.pdf.write_to_path(pdf_path)

    def test_draw_with_top_margin(self):
        self.hls.top_margin = 15

        with self.file_path(parent_path=path, name='draw_with_top_margin', extension='pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(10, 10)

            self.hls.end_mark_line.show = True
            self.hls.draw(self.pdf)

            self.pdf.write_to_path(pdf_path)

    def test_end_mark_line_labels(self):
        self.hls.end_mark_line.add_label('end mark line')
        with self.file_path(parent_path=path, name='end_mark_line_labels', extension='pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(10, 10)

            self.hls.end_mark_line.show = True
            self.hls.draw(self.pdf)

            self.pdf.write_to_path(pdf_path)
