from pathlib import Path

from musurgia.pdf.pdf import Pdf
from musurgia.unittest import TestCase, create_test_path

path = Path(__file__)


class TestVerticalLineSegment(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_draw(self):
        pdf_path = create_test_path(path, 'draw.pdf')
        vl = VerticalLineSegment()

        self.pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)
