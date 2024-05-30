from pathlib import Path

from musurgia.musurgia_exceptions import RelativePositionNotSettableError
from musurgia.pdf.line import StraightLine
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.tests._test_utils import PdfTestCase, DummyMaster

path = Path(__file__)


class TestStraightLine(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.master = DummyMaster()
        self.sl = StraightLine(mode='h', length=20, name='straight_test', master=self.master)

    def test_position_not_settable(self):
        with self.assertRaises(RelativePositionNotSettableError):
            StraightLine(relative_x=0, mode='h', length=20, name='straight_test', master=self.master)
        with self.assertRaises(RelativePositionNotSettableError):
            self.sl.relative_x = 10

    def test_relative_x(self):
        actual = self.sl.relative_x
        expected = self.master.get_slave_position(self.sl, 'x')
        self.assertEqual(expected, actual)

    def test_get_relative_x(self):
        actual = self.sl.get_relative_x2()
        expected = self.sl.relative_x + self.sl.length
        self.assertEqual(expected, actual)

    def test_get_width(self):
        actual = self.sl.get_width()
        expected = self.sl.left_margin + self.sl.length + self.sl.right_margin
        self.assertEqual(expected, actual)

    def test_get_height(self):
        actual = self.sl.get_height()
        expected = self.sl.top_margin + self.sl.bottom_margin
        self.assertEqual(expected, actual)

    def test_draw(self):
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.sl.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
