from pathlib import Path

from musurgia.pdf.line import HorizontalLineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.unittest import TestCase

path = Path(__file__)


class TestMarkLineLabels(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.ls = HorizontalLineSegment(length=20)

    # def test_position_x_above(self):
    #     ml = self.ls.end_mark_line
    #     tl = ml.add_text_label('first value label above')
    #     actual = tl.relative_x
    #     expected = ml.relative_x
    #     self.assertEqual(expected, actual)

    # def test_position_y_second_above(self):
    #     ml = self.ls.end_mark_line
    #     tl1 = ml.add_text_label('first value label above')
    #     tl2 = ml.add_text_label('second value label above')
    #     actual = tl1.relative_y
    #     expected = ml.relative_y
    #
    #     self.assertEqual(expected, actual)

    def test_draw_above(self):
        ml = self.ls.start_mark_line
        ml.add_text_label('first text label above')
        ml.add_text_label('second text label above')
        ml.add_text_label('third  text label above')
        self.ls.relative_x = 10
        self.ls.relative_y = 20
        with self.file_path(path, 'draw_above', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')

            self.ls.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_draw_below(self):
        ml = self.ls.start_mark_line
        ml.add_text_label('first text label below', placement='below')
        ml.add_text_label('second text label below', placement='below')
        self.ls.relative_x = 10
        self.ls.relative_y = 20
        with self.file_path(path, 'draw_below', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.ls.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_draw_left(self):
        ml = self.ls.start_mark_line
        ml.add_text_label('first text label left', placement='left')
        ml.add_text_label('second text label left left left', placement='left')
        ml.add_text_label('third text label left left left', placement='left')
        for text_label in ml.left_text_labels:
            text_label.right_margin = 2
            text_label.top_margin = -2
        ml.left_text_labels[1].font.size = 8
        self.ls.relative_x = 40
        self.ls.relative_y = 10
        with self.file_path(path, 'draw_left', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.ls.draw(self.pdf)
            self.pdf.write(pdf_path)

    # def test_get_height(self):
    #     ml = self.ls.start_mark_line
    #     ml.add_text_label('first text label above')
    #     ml.add_text_label('second text label above')
    #     print(ml.get_height())

