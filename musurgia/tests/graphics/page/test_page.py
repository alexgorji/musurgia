from pathlib import Path
from unittest import TestCase
from musurgia.graphics.page import Page
from musurgia.tests.helpers.svg import SVGTestCase, SVG
import xml.etree.ElementTree as ET

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

    def test_empty_page_to_svg(self):
        page = Page()
        svg_xml = page.convert_to_svg_string()
        root = ET.fromstring(svg_xml)
        assert root.attrib["width"] == "210mm"
        assert root.attrib["height"] == "297mm"
        assert root.attrib["viewBox"] == "0 0 210 297"

    def test_add_text_to_page(self):
        page = Page()
        page.add_text("some text")
        assert "some text" in page.convert_to_svg_string()


class GraphicPageRegressionTests(SVGTestCase):
    def test_empty_page(self):
        page = Page()

        svg_path = SVG(page.convert_to_svg_string()).write_to_path(
            self.create_test_path(this_path, "empty_page", "svg")
        )

        png_path = self.create_test_path(this_path, "empty_page", "png")

        self.compare_svg_to_png(
            svg_path,
            png_path,
            page.layout.get_size()["width"],
            page.layout.get_size()["height"],
        )

    def test_add_text_to_page(self):
        page = Page()
        page.add_text("some text", relative_x=10, relative_y=20, color="blue")

        svg_path = SVG(page.convert_to_svg_string()).write_to_path(
            self.create_test_path(this_path, "add_text", "svg")
        )

        png_path = self.create_test_path(this_path, "add_text", "png")

        self.compare_svg_to_png(
            svg_path,
            png_path,
            page.layout.get_size()["width"],
            page.layout.get_size()["height"],
            tolerance=0.002,
        )
