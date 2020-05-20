from pathlib import Path

from musurgia.pdf.pdf import Pdf
from musurgia.pdf.text import Text
from musurgia.unittest import TestCase

path = Path(__file__)


class TestText(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_draw(self):
        t = Text('fox is going to be dead.')
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            t.draw(self.pdf)
            self.pdf.write(pdf_path)
