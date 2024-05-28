from pathlib import Path

from musurgia.pdf.line import HorizontalRuler
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.tests._test_utils import TestCase

path = Path(__file__)


class TestRuler(TestCase):
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
