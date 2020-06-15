from pathlib import Path

from musurgia.pdf.line import HorizontalLineSegment, VerticalLineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.unittest import TestCase

path = Path(__file__)


class TestStraightLineLabels(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.hls = HorizontalLineSegment(length=20)
        self.hls.start_mark_line.show = False
        self.vls = VerticalLineSegment(length=20)
        self.vls.start_mark_line.show = False

    def test_horizontal_above(self):
        self.hls.straight_line.add_text_label('one above')
        self.hls.straight_line.add_text_label('two above')
        self.hls.straight_line.add_text_label('three above')
        with self.file_path(path, 'horizontal_above', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(20, 20)
            self.hls.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_horizontal_below(self):
        self.hls.straight_line.add_text_label('one below', placement='below')
        self.hls.straight_line.add_text_label('two below', placement='below')
        self.hls.straight_line.add_text_label('three below', placement='below')
        with self.file_path(path, 'test_horizontal_below', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(20, 20)
            self.hls.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_horizontal_left(self):
        self.hls.straight_line.add_text_label('one left', placement='left')
        self.hls.straight_line.add_text_label('two left', placement='left')
        self.hls.straight_line.add_text_label('three left', placement='left')
        with self.file_path(path, 'horizontal_left', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(20, 20)
            self.hls.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_vertical_above(self):
        self.vls.straight_line.add_text_label('one above')
        self.vls.straight_line.add_text_label('two above')
        self.vls.straight_line.add_text_label('three above')
        with self.file_path(path, 'vertical_above', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(20, 20)
            self.vls.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_vertical_above_with_relative_y(self):
        self.vls.relative_y = -10
        # print(self.vls.straight_line.relative_y)
        self.vls.straight_line.add_text_label('one above')
        self.vls.straight_line.add_text_label('two above')
        self.vls.straight_line.add_text_label('three above')
        with self.file_path(path, 'vertical_above_with_relative_y', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(20, 20)
            self.vls.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_vertical_below(self):
        t1 = self.vls.straight_line.add_text_label('one below', placement='below')
        t2 = self.vls.straight_line.add_text_label('two below', placement='below')
        t3 = self.vls.straight_line.add_text_label('three below', placement='below')
        t1.top_margin = t1.get_text_height()
        t2.top_margin = sum([t.get_text_height() for t in [t1, t2]])
        t3.top_margin = sum([t.get_text_height() for t in [t1, t2, t3]])

        with self.file_path(path, 'test_vertical_below', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(20, 20)
            self.vls.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_vertical_left(self):
        self.vls.straight_line.add_text_label('one left', placement='left')
        self.vls.straight_line.add_text_label('two left', placement='left')
        self.vls.straight_line.add_text_label('three left', placement='left')
        with self.file_path(path, 'vertical_left', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(20, 20)
            self.vls.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_vertical_left_with_top_margin(self):
        self.vls.top_margin = 20
        self.vls.straight_line.add_text_label('one left', placement='left')
        self.vls.straight_line.add_text_label('two left', placement='left')
        self.vls.straight_line.add_text_label('three left', placement='left')
        with self.file_path(path, 'vertical_left_with_top_margin', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(20, 20)
            self.vls.draw(self.pdf)
            self.pdf.write(pdf_path)
