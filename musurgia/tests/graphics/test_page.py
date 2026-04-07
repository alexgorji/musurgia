from pathlib import Path
from unittest import TestCase
from musurgia.graphics.geometry import Size
from musurgia.graphics.page import Page

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
