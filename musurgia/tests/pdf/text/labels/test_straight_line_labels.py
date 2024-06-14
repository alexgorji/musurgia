from pathlib import Path

from musurgia.pdf import Pdf, StraightLine, draw_ruler
from musurgia.tests.utils_for_tests import PdfTestCase, add_test_labels

path = Path(__file__)


class TestStraightLineLabels(PdfTestCase):
    def setUp(self):
        self.pdf = Pdf()
        self.line = StraightLine(length=30, mode='h')
        self.line.positions = (5, 5)
        self.line.margins = (5, 10, 15, 20)

    def test_straight_line_labels(self):
        add_test_labels(self.line)
        with self.file_path(path, 'straight_line_labels', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'v')
            draw_ruler(self.pdf, 'h')
            self.pdf.translate(10, 10)
            self.line.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
