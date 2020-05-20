from pathlib import Path

from musurgia.pdf.line import HorizontalLineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.unittest import TestCase

path = Path(__file__)


class TestHorizontalLineSegment(TestCase):
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
        expected = self.hls.relative_y
        self.assertEqual(expected, actual)

    def test_end_mark_line_relative_x(self):
        actual = self.hls.end_mark_line.relative_x
        expected = self.hls.relative_x + self.hls.length
        self.assertEqual(expected, actual)

    def test_end_mark_line_relative_y(self):
        actual = self.hls.end_mark_line.relative_y
        expected = self.hls.relative_y
        self.assertEqual(expected, actual)

    def test_draw(self):
        with self.file_path(parent_path=path, name='draw', extension='pdf') as pdf_path:
            self.pdf.translate_margins()
            self.hls.end_mark_line.show = True
            self.hls.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_draw_list(self):
        segments = [HorizontalLineSegment(length) for length in range(10, 30, 5)]
        segments[-1].end_mark_line.show = True
        with self.file_path(parent_path=path, name='draw_list', extension='pdf') as pdf_path:
            self.pdf.translate_margins()
            # with self.pdf.saved_state():
            for segment in segments:
                segment.draw(self.pdf)
                self.pdf.translate(segment.get_width(), -segment.get_height())

            self.pdf.write(pdf_path)
