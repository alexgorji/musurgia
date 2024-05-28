from unittest import TestCase

from musurgia.pdf.drawobject import ClippingArea
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.line import HorizontalRuler


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