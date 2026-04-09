from pathlib import Path
from unittest import TestCase
from musurgia.graphics.geometry import Size
from musurgia.graphics.page_layout import PageLayout
from musurgia.graphics.svg.paginator import SVGPage

this_path = Path(__file__)


class GraphicPageTestCase(TestCase):
    def test_page_layout_size(self):
        page = SVGPage()
        assert page.get_layout().size == "A4"
        assert page.get_layout().orientation == "portrait"
        assert page.get_layout().get_size() == Size(210, 297)
        page = SVGPage(layout=PageLayout(orientation="landscape"))
        assert page.get_layout().orientation == "landscape"
        assert page.get_layout().get_size() == Size(297, 210)

        page = SVGPage(layout=PageLayout(size="A3"))
        assert page.get_layout().size == "A3"
        assert page.get_layout().get_size() == Size(297, 420)

        page = SVGPage(layout=PageLayout(size="A3", orientation="landscape"))
        assert page.get_layout().get_size() == Size(420, 297)
