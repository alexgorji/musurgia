from pathlib import Path

from musurgia.pdf.drawobjectgroup import DrawObjectGroup
from musurgia.pdf.pdf import Pdf
from musurgia.unittest import TestCase, create_path

path = Path(__file__)


class Test(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf(orientation='l')

    def test_draw(self):
        pdf_path = create_path(path, 'draw.pdf')
        slg = DrawObjectGroup()
        self.pdf.write(pdf_path)
