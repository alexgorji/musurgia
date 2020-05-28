from math import ceil
from pathlib import Path

from musurgia.pdf.line import HorizontalRuler
from musurgia.pdf.pdf import Pdf
from musurgia.unittest import TestCase, create_test_path

path = Path(__file__)


class TestClip(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_line(self):
        pdf_path = create_test_path(path, 'line.pdf')
        self.pdf.rect(0, 0, 50, 50)
        self.pdf.clip_rect(0, 0, 50, 50)
        self.pdf.line(10, 20, 100, 100)
        self.pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)

    def test_line_break(self):
        def draw_with_clip(index):
            with self.pdf.saved_state():
                self.pdf.clip_rect(-1, -5, 196, 50)
                self.pdf.translate(index * -190, 0)
                ruler.draw(self.pdf)

        ruler = HorizontalRuler(length=800, unit=10)
        with self.file_path(path, 'line_break', 'pdf') as pdf_path:
            self.pdf.translate(10, 10)
            number_of_rows = int(ceil(ruler.length / 190))
            for index in range(number_of_rows):
                if index != 0:
                    self.pdf.translate(0, 30)
                draw_with_clip(index)
            self.pdf.write(pdf_path)
