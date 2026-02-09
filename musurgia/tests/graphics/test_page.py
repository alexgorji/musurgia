from pathlib import Path
from unittest import TestCase
from musurgia.graphics.drawobject import Size
from musurgia.graphics.page import Margins, Page

this_path = Path(__file__)


class GraphicPageTestCase(TestCase):
    def test_page_layout_size(self):
        page = Page()
        assert page.layout.size == "A4"
        assert page.layout.orientation == "portrait"
        assert page.layout.get_size() == Size(210, 297)
        page.layout.orientation = "landscape"
        assert page.layout.orientation == "landscape"
        assert page.layout.get_size() == Size(297, 210)

        page.layout.size = "A3"
        assert page.layout.size == "A3"
        page.layout.orientation = "portrait"
        assert page.layout.get_size() == Size(297, 420)

        page.layout.orientation = "landscape"
        assert page.layout.get_size() == Size(420, 297)

    def test_page_layout_margins(self):
        page = Page()
        assert page.layout.margins == Margins(0, 0, 0, 0)
        page.layout.margins.top = 10
        page.layout.margins.bottom = 20
        page.layout.margins.left = 30
        page.layout.margins.right = 40
        assert page.layout.margins == Margins(10, 40, 20, 30)
