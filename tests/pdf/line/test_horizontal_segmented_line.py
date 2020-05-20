from pathlib import Path

from musurgia.pdf.line import HorizontalSegmentedLine
from musurgia.pdf.pdf import Pdf
from musurgia.unittest import TestCase

path = Path(__file__)


class TestHorizontalSegmentedLine(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.hsl = HorizontalSegmentedLine(lengths=[10, 15, 20, 25])

    def test_draw(self):
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            self.pdf.translate(self.pdf.l_margin, self.pdf.t_margin)
            self.hsl.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_labeled(self):
        for index, segment in enumerate(self.hsl.segments):
            segment.add_label()

        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            self.pdf.translate(self.pdf.l_margin, self.pdf.t_margin)
            self.hsl.draw(self.pdf)
            self.pdf.write(pdf_path)
