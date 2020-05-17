from pathlib import Path

from musurgia.pdf.pdf import Pdf
from musurgia.pdf.positioned import RelativeXNotSettableError
from musurgia.pdf.segmentedline import LineSegment, MarkLine
from musurgia.unittest import TestCase, create_path

path = Path(__file__)


class Test(TestCase):
    def setUp(self) -> None:
        self.line_segment = LineSegment(10, relative_x=11, relative_y=12, bottom_margin=13, left_margin=14,
                                        top_margin=15,
                                        right_margin=16)

        self.pdf = Pdf()

    def test_relative_set_error(self):
        mk = MarkLine(parent=self.line_segment, placement='start')
        with self.assertRaises(RelativeXNotSettableError):
            mk.relative_x = 20

    def test_relative_x_start(self):
        mk = MarkLine(parent=self.line_segment, placement='start')
        expected = self.line_segment.relative_x
        actual = mk.relative_x
        self.assertEqual(expected, actual)

    def test_relative_x_end(self):
        mk = MarkLine(parent=self.line_segment, placement='end')
        expected = self.line_segment.relative_x + self.line_segment.length
        actual = mk.relative_x
        self.assertEqual(expected, actual)

    def test_relative_y(self):
        mk = MarkLine(parent=self.line_segment)
        expected = self.line_segment.relative_y
        actual = mk.relative_y
        self.assertEqual(expected, actual)

    def test_draw_start(self):
        pdf_path = create_path(path, 'draw_start_mark_line.pdf')
        mk = MarkLine(parent=self.line_segment, placement='start')
        mk.draw(self.pdf)
        self.line_segment.relative_x += 20
        self.line_segment.relative_y += 20
        mk.draw(self.pdf)
        self.pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)

    def test_draw_end(self):
        pdf_path = create_path(path, 'draw_end_mark_line.pdf')
        mk = MarkLine(parent=self.line_segment, placement='end')
        mk.draw(self.pdf)
        self.line_segment.relative_x += 20
        self.line_segment.relative_y += 20
        mk.draw(self.pdf)
        self.pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)

    def test_get_height(self):
        self.line_segment.relative_y = 10
        mk = MarkLine(parent=self.line_segment, placement='end')
        actual = mk.get_height()
        expected = mk.height
        self.assertEqual(expected, actual)
