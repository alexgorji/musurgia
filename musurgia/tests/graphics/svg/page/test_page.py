from pathlib import Path
from unittest import TestCase
from musurgia.graphics.drawobject import DrawObjectLayout, TextDrawObject
from musurgia.graphics.page import Page
from musurgia.tests.helpers.svg import SVGTestCase, SVG
import xml.etree.ElementTree as ET

this_path = Path(__file__)


class PageToSVGTestCase(TestCase):
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

    def test_add_multiple_draw_objects_to_page(self):
        page = Page()
        page.add_draw_object(
            TextDrawObject(
                "Hello", layout=DrawObjectLayout(relative_x=10, relative_y=10)
            )
        )

        page.add_draw_object(
            TextDrawObject(
                "Goodbye", layout=DrawObjectLayout(relative_x=20, relative_y=20)
            )
        )
        svg_string = page.convert_to_svg_string()
        assert "Hello" in svg_string
        assert "Goodbye" in svg_string


class PageToSVGRegressionTests(SVGTestCase):
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

    def test_add_draw_object_to_page(self):
        page = Page()
        page.add_draw_object(
            TextDrawObject(
                text="some text",
                layout=DrawObjectLayout(relative_x=10, relative_y=20),
                color="blue",
            )
        )

        svg_path = SVG(page.convert_to_svg_string()).write_to_path(
            self.create_test_path(this_path, "add_draw_object", "svg")
        )

        png_path = self.create_test_path(this_path, "add_draw_object", "png")

        self.compare_svg_to_png(
            svg_path,
            png_path,
            page.layout.get_size()["width"],
            page.layout.get_size()["height"],
            tolerance=0.002,
        )
