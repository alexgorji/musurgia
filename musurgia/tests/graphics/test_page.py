from pathlib import Path
from unittest import TestCase
from musurgia.graphics.page import Page

this_path = Path(__file__)


class GraphicPageTestCase(TestCase):
    def test_page_layout_size(self):
        page = Page()
        assert page.layout.size == "A4"
        assert page.layout.orientation == "portrait"
        assert page.layout.get_size() == {"height": 297, "width": 210}

        page.layout.orientation = "landscape"
        assert page.layout.orientation == "landscape"
        assert page.layout.get_size() == {"height": 210, "width": 297}

        page.layout.size = "A3"
        assert page.layout.size == "A3"
        page.layout.orientation = "portrait"
        assert page.layout.get_size() == {"height": 420, "width": 297}

        page.layout.orientation = "landscape"
        assert page.layout.get_size() == {"height": 297, "width": 420}

    def test_page_layout_margins(self):
        page = Page()
        assert page.layout.margins == {"left": 0, "right": 0, "bottom": 0, "top": 0}
        page.layout.margins["top"] = 10
        page.layout.margins["bottom"] = 20
        page.layout.margins["left"] = 30
        page.layout.margins["right"] = 40
        assert page.layout.margins == {
            "top": 10,
            "bottom": 20,
            "left": 30,
            "right": 40,
        }
