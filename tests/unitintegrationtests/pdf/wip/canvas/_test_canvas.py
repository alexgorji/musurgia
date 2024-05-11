from pathlib import Path

from musurgia.pdf.canvas import Canvas
from musurgia.pdf.pdf import Pdf
from tests.unitintegrationtests.test_utils  import TestCase, create_test_path

path = Path(__file__)


class TestCanvas(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_empty_draw(self):
        pdf_path = create_test_path(path, 'empty_draw.pdf')
        canvas = Canvas()
        canvas.draw(self.pdf)
        self.pdf.write_to_path(pdf_path)
        self.assertCompareFiles(pdf_path)
