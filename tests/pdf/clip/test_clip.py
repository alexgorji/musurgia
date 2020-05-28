from pathlib import Path

from musurgia.pdf.line import HorizontalLineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.rowcolumn import DrawObjectRow
from musurgia.unittest import TestCase, create_test_path

path = Path(__file__)


class Ruler(DrawObjectRow):
    def __init__(self, length, unit, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fill_segments(length, unit)

    def _fill_segments(self, length, unit):
        for i in range(int(length / unit)):
            hls = self.add_draw_object(HorizontalLineSegment(unit))
            hls.start_mark_line.add_label(i)


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
        pdf = Pdf()

        ruler = Ruler(length=700, unit=10)
        print(ruler.get_width())

        pdf_path = create_test_path(path, 'line_break.pdf')
        pdf.translate(10, 10)
        with pdf.saved_state():
            pdf.clip_rect(-1, -5, 196, 50)
            ruler.draw(pdf)

        pdf.translate(0, 30)

        with pdf.saved_state():
            pdf.clip_rect(-1, -5, 195, 50)
            pdf.translate(-190, 0)
            ruler.draw(pdf)

        pdf.translate(0, 30)
        with pdf.saved_state():
            pdf.clip_rect(-1, -5, 195, 50)
            pdf.translate(-380, 0)
            ruler.draw(pdf)

        pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)
