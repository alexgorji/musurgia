import copy
from pathlib import Path

from fpdf.drawing import Line

from musurgia.pdf import DrawObjectRow
from musurgia.pdf.line import HorizontalSegmentedLine
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestHorizontalSegmentedLine(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.hsl = HorizontalSegmentedLine(lengths=[10, 15, 20, 25])

    def test_segments(self):
        assert [seg.length for seg in self.hsl.segments] == [10, 15, 20, 25]
        assert self.hsl.segments[-1].end_mark_line.show is True
        assert set([seg.end_mark_line.show for seg in self.hsl.segments[:-1]]) == {False}
        assert set([seg.start_mark_line.show for seg in self.hsl.segments]) == {True}

    def test_draw(self):
        with self.file_path(parent_path=path, name='draw', extension='pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.hsl.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_get_height(self):
        self.hsl.segments[1].start_mark_line.length = 5
        assert self.hsl.get_height() == 5

    def test_add_label_left(self):
        self.hsl.add_label('first left label', placement='left')
        self.hsl.add_label('second left label', placement='left')
        self.hsl.add_label('third left label', placement='left')
        self.hsl.add_label('fourth left label', placement='left')
        self.hsl.segments[0].start_mark_line.length = 10
        self.pdf.translate_page_margins()
        self.pdf.translate(40, 20)
        self.hsl.draw(self.pdf)
        with self.file_path(path, 'add_label_left', 'pdf') as pdf_path:
            self.pdf.write_to_path(pdf_path)

    def test_change_markline_lengths(self):
        assert set([sg.start_mark_line.length for sg in self.hsl.segments] + [sg.end_mark_line.length for sg in
                                                                              self.hsl.segments]) == {3}
        for index, sg in enumerate(self.hsl.segments):
            sg.start_mark_line.length += index * 5
        self.hsl.segments[-1].end_mark_line.length = self.hsl.segments[-1].start_mark_line.length + 5
        self.hsl.segments[-1].end_mark_line.show = True

        assert set([sg.relative_y for sg in self.hsl.segments]) == {0}

        with self.file_path(path, 'change_markline_lengths', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.translate(0, 30)
            for sg in self.hsl.segments:
                copied = copy.deepcopy(sg)
                copied.straight_line.add_text_label(f'{copied.straight_line.get_positions()}', font_size=5, placement='below')
                copied.start_mark_line.add_text_label(f'{copied.start_mark_line.get_positions()}', font_size=5,
                                                      placement='above')
                copied.draw(self.pdf)
                self.pdf.translate(30, 0)
            self.pdf.reset_position()
            self.pdf.translate_page_margins()
            self.pdf.translate(0, 60)
            self.hsl.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
