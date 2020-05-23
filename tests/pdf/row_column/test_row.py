from pathlib import Path

from musurgia.pdf.pdf import Pdf
from musurgia.unittest import TestCase

path = Path(__file__)


class TestRow(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf(orientation='l')

    def draw(self):
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            r = PdfRow()
            r.draw(self.pdf)

