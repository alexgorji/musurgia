from pathlib import Path

from musurgia.pdf.line import HorizontalLineSegment, HorizontalSegmentedLine, VerticalSegmentedLine
from musurgia.pdf.pdf import Pdf
from musurgia.unittest import TestCase

path = Path(__file__)


class TestMarkLineLabels(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.ls = HorizontalLineSegment(length=20)

    def test_position_x_above(self):
        ml = self.ls.end_mark_line
        tl = ml.add_text_label('first value label above')
        actual = tl.relative_x
        expected = ml.relative_x
        self.assertEqual(expected, actual)

    def test_position_y_second_above(self):
        ml = self.ls.end_mark_line
        tl1 = ml.add_text_label('first value label above')
        tl2 = ml.add_text_label('second value label above')
        actual = tl1.relative_y
        expected = ml.relative_y

        self.assertEqual(expected, actual)

    def test_draw_above(self):
        ruler_1 = HorizontalSegmentedLine(lengths=10 * [10])
        ruler_2 = VerticalSegmentedLine(lengths=10 * [10])
        ml = self.ls.start_mark_line
        ml.add_text_label('first text label above')
        ml.add_text_label('second text label above')
        ml.add_text_label('third  text label above')

        with self.file_path(path, 'draw_above', 'pdf') as pdf_path:
            with self.pdf.saved_state():
                ruler_1.draw(self.pdf)
            with self.pdf.saved_state():
                ruler_2.draw(self.pdf)
            self.pdf.translate_page_margins()
            self.ls.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_draw_below(self):
        ruler_1 = HorizontalSegmentedLine(lengths=10 * [10])
        ruler_2 = VerticalSegmentedLine(lengths=10 * [10])
        ml = self.ls.start_mark_line
        ml.add_text_label('first text label below', placement='below')
        ml.add_text_label('second text label below', placement='below')

        with self.file_path(path, 'draw_below', 'pdf') as pdf_path:
            with self.pdf.saved_state():
                ruler_1.draw(self.pdf)
            with self.pdf.saved_state():
                ruler_2.draw(self.pdf)
            self.pdf.translate_page_margins()
            self.ls.draw(self.pdf)
            self.pdf.write(pdf_path)


