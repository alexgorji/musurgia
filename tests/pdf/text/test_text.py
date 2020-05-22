from pathlib import Path

from musurgia.pdf.line import HorizontalLineSegment, HorizontalSegmentedLine, VerticalSegmentedLine
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.text import Text
from musurgia.unittest import TestCase

path = Path(__file__)


class TestText(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_draw(self):
        t = Text('The fox is going to be dead.')
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            t.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_draw_with_top_margin(self):
        t = Text('The fox is going to be dead.')
        t.top_margin = 2
        with self.file_path(path, 'draw_with_top_margin', 'pdf') as pdf_path:
            with self.pdf.saved_state():
                HorizontalSegmentedLine(lengths=10 * [10]).draw(self.pdf)
            with self.pdf.saved_state():
                VerticalSegmentedLine(lengths=10 * [10]).draw(self.pdf)
            self.pdf.translate_page_margins()
            t.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_get_height(self):
        t = Text('fox is going to be dead.')
        t.font_size = 14
        t.top_margin = 3
        expected = 7.682066666666666
        actual = t.get_height()
        self.assertEqual(expected, actual)

    def test_height_graphical(self):
        t = Text('The fox is going to be dead.')
        with self.file_path(path, 'height_graphical', 'pdf') as pdf_path:
            ruler1 = HorizontalSegmentedLine(lengths=10 * [10])
            ruler2 = VerticalSegmentedLine(lengths=10 * [10])
            with self.pdf.saved_state():
                ruler1.draw(self.pdf)
            with self.pdf.saved_state():
                ruler2.draw(self.pdf)

            self.pdf.translate_page_margins()

            hls = HorizontalLineSegment(length=t.get_text_width(), relative_y=-t.get_text_height() * 3/4)
            hls.start_mark_line.length = t.get_height()
            hls.end_mark_line.show = True

            with self.pdf.saved_state():
                self.pdf.rect(hls.relative_x, hls.relative_y, hls.get_width(), t.get_height())
                hls.draw(self.pdf)
            t.draw(self.pdf)

            self.pdf.write(pdf_path)

    def test_draw_multiple(self):
        t1 = Text(value='Fox is going to be dead.')
        t2 = Text(value='What should we do??', relative_y=0)
        t3 = Text(value='What should we do??', relative_y=0)
        with self.file_path(path, 'draw_multiple', 'pdf') as pdf_path:
            with self.pdf.saved_state():
                HorizontalSegmentedLine(10 * [10], relative_y=1.5).draw(self.pdf)
            with self.pdf.saved_state():
                VerticalSegmentedLine(10 * [10]).draw(self.pdf)
            self.pdf.translate_page_margins()
            t1.draw(self.pdf)
            self.pdf.translate(0, t1.get_height())
            t2.draw(self.pdf)
            self.pdf.translate(0, t1.get_height())
            t3.draw(self.pdf)
            self.pdf.translate(0, t1.get_height())
            self.pdf.write(pdf_path)

    def test_draw_multiple_saved_state(self):
        t1 = Text(value='Fox is going to be dead.')
        t2 = Text(value='What should we do??', relative_y=10)
        t3 = Text(value='What should we do??', relative_y=20)
        with self.file_path(path, 'draw_multiple_saved_state', 'pdf') as pdf_path:
            with self.pdf.saved_state():
                HorizontalSegmentedLine(10 * [10]).draw(self.pdf)
            with self.pdf.saved_state():
                VerticalSegmentedLine(10 * [10]).draw(self.pdf)
            self.pdf.translate_page_margins()
            with self.pdf.saved_state():
                t1.draw(self.pdf)
            with self.pdf.saved_state():
                t2.draw(self.pdf)
            with self.pdf.saved_state():
                t3.draw(self.pdf)
            self.pdf.write(pdf_path)