from pathlib import Path
from unittest import TestCase

from musurgia.musurgia_exceptions import RulerCannotSetLengthsError, SegmentedLineLengthsCannotBeSetError
from musurgia.pdf.ruler import HorizontalRuler, TimeRuler
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestRuler(TestCase):
    def setUp(self) -> None:
        self.r = HorizontalRuler(length=100)

    def test_setting_length_and_lengths(self):
        with self.assertRaises(RulerCannotSetLengthsError):
            HorizontalRuler(lengths=[3, 2, 1], length=100)

        with self.assertRaises(SegmentedLineLengthsCannotBeSetError):
            self.r.lengths = [3, 2, 1]


class TestTimeRuler(TestCase):
    def setUp(self) -> None:
        self.tr = TimeRuler(duration=200, unit=2, label_show_interval=10, shrink_factor=0.6, mark_line_length=5)

    def test_duration(self):
        assert self.tr.duration == 200
        assert self.tr.unit == 2
        assert self.tr.length == 400

    def test_shrink(self):
        assert self.tr.shrink_factor == 0.6
        assert self.tr.mark_line_length == 5
        for i, start_mark_line in enumerate([seg.start_mark_line for seg in self.tr.segments]):
            if i % 10 == 0:
                assert start_mark_line.length == 5
            else:
                assert start_mark_line.length == 3

        self.tr.mark_line_length = 10
        self.tr.shrink_factor = 0.5
        for i, start_mark_line in enumerate([seg.start_mark_line for seg in self.tr.segments]):
            if i % 10 == 0:
                assert start_mark_line.length == 10
            else:
                assert start_mark_line.length == 5

        self.tr.label_show_interval = 3
        for i, start_mark_line in enumerate([seg.start_mark_line for seg in self.tr.segments]):
            if i % 3 == 0:
                assert start_mark_line.length == 10
            else:
                assert start_mark_line.length == 5


class TestRulerPdf(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_h_ruler(self):
        r = HorizontalRuler(length=50)
        with self.file_path(path, 'h_ruler', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            r.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_h_ruler_A4(self):
        with self.file_path(path, 'h_ruler_A4', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, mode='h')
            self.pdf.write_to_path(pdf_path)

    def test_both_rulers_A4(self):
        with self.file_path(path, 'both_rulers_A4', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, mode='h')
            draw_ruler(self.pdf, mode='v')
            self.pdf.write_to_path(pdf_path)

    def test_rulers_borders_and_margins(self):
        with self.file_path(path, 'both_rulers_borders_and_margins', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, mode='h', show_borders=True, show_margins=True)
            draw_ruler(self.pdf, mode='v', show_borders=True, show_margins=True)
            self.pdf.write_to_path(pdf_path)

    def test_time_ruler(self):
        r = TimeRuler(length=1000, unit=2, label_show_interval=10)
        for l in [label for seg in r.segments for label in seg.start_mark_line.get_text_labels()]:
            l.font_size = 5
        r.bottom_margin = 15
        with self.file_path(path, 'time_ruler', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            r.clipped_draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
