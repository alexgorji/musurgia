from pathlib import Path

from musurgia.pdf.pdf import Pdf
from musurgia.unittest import TestCase, create_test_path

path = Path(__file__)


class Test(TestCase):
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
        pdf = Pdf(unit='pt')

        def draw_scene():
            pdf.line(0, 0, 300, 50)
            pdf.rect(0, 0, 20, 30)
            pdf.rect(50, 20, 2, 3)
            pdf.rect(152, 28, 4, 6)
            pdf.line(300, 50, 600, 0)

        pdf_path = create_test_path(path, 'line_break.pdf')
        pdf.translate(20, -20)

        pdf.rect(0, 0, 150, 50)
        draw_scene()

        pdf.translate(0, -100)
        pdf.rect(0, 0, 150, 50)
        with pdf.saved_state():
            pdf.clip_rect(0, 0, 150, 50)
            pdf.translate(-150, 0)
            pdf.set_draw_color(255, 0, 0)
            draw_scene()

        pdf.translate(0, -100)
        pdf.rect(0, 0, 150, 50)
        with pdf.saved_state():
            pdf.clip_rect(0, 0, 150, 50)
            pdf.translate(-300, 0)
            pdf.set_draw_color(0, 0, 255)
            draw_scene()

        pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)
