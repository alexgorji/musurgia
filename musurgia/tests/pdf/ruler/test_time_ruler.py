from pathlib import Path
from unittest import TestCase

from musurgia.pdf import Pdf, DrawObjectColumn
from musurgia.pdf.ruler import TimeRuler
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestTimeRuler(TestCase):
    def test_time_ruler_duration(self):
        assert False


class TestTimeRulerDraw(PdfTestCase):
    def setUp(self):
        self.pdf = Pdf(orientation='landscape')

    def test_time_ruler(self):
        c = DrawObjectColumn()
        tr = TimeRuler(duration=125)
        c.add_draw_object(tr)
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            c.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
