from pathlib import Path

from musurgia.pdf.line import HorizontalLine
from musurgia.pdf.pdf import Pdf
from musurgia.unittest import TestCase, create_test_path

path = Path(__file__)


class Test(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_draw(self):
        pdf_path = create_test_path(path, 'draw.pdf')
        hl = HorizontalLine(length=20, top_margin=20, left_margin=30)
        hl.end_mark_line.show = True
        hl.draw(self.pdf)
        self.pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)
