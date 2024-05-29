from unittest import TestCase

from musurgia.musurgia_exceptions import PdfAttributeError
from musurgia.musurgia_types import MusurgiaTypeError
from musurgia.pdf.drawobject import ClippingArea
from musurgia.pdf.line import HorizontalRuler
from musurgia.pdf.masterslave import SimpleNamed, Slave
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.pdf.pdfunit import PdfUnit


class TestClippingArea(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.ruler = HorizontalRuler(length=2000)
        self.ca = ClippingArea(self.pdf, self.ruler)

    def test_get_row_height(self):
        x = self.ruler.get_height()
        assert self.ca.get_row_height() == x
        self.ruler.top_margin = 10
        assert self.ca.get_row_height() == x + 10

    def test_no_pdf(self):
        with self.assertRaises(PdfAttributeError):
            ClippingArea(pdf=None, draw_object=self.ruler).get_row_height()
        with self.assertRaises(PdfAttributeError):
            ClippingArea(pdf=None, draw_object=self.ruler).get_row_width()


class TestSimpleNamed(TestCase):
    def test_wrong_type(self):
        with self.assertRaises(MusurgiaTypeError):
            SimpleNamed(3)


class TestSlave(TestCase):
    def test_wrong_master_type(self):
        with self.assertRaises(MusurgiaTypeError):
            Slave(master='bla')


class TestPdfUnit(TestCase):
    def test_setting_global_unit(self):
        assert PdfUnit._DEFAULT_UNIT == 'mm'
        assert PdfUnit.GLOBAL_UNIT == 'mm'
        PdfUnit.GLOBAL_UNIT = 'pt'
        assert PdfUnit.GLOBAL_UNIT == 'pt'
        PdfUnit.reset()
        assert PdfUnit.GLOBAL_UNIT == 'mm'
        with self.assertRaises(MusurgiaTypeError):
            PdfUnit.GLOBAL_UNIT = 'bla'

# class TestDrawObject(TestCase):
#     def test_no_margins(self):
#         class Dummy(DrawObject):
#             pass
#
#         d = Dummy()
