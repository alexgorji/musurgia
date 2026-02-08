from pathlib import Path
from unittest import TestCase

from musurgia.graphics.drawobject import (
    HorizontalLineDrawObject,
    Position,
    TextDrawObject,
    VerticalLineDrawObject,
)
from musurgia.graphics.page import Page
from musurgia.tests.helpers.svg import SVGTestCase
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
        page.add_draw_object(TextDrawObject(text="some text"))
        assert "some text" in page.convert_to_svg_string()

    def test_add_multiple_draw_objects_to_page(self):
        page = Page()
        page.add_draw_object(TextDrawObject(text="Hello", start=Position(10, 10)))

        page.add_draw_object(TextDrawObject(text="Goodbye", start=Position(20, 20)))

        svg_string = page.convert_to_svg_string()
        assert "Hello" in svg_string
        assert "Goodbye" in svg_string


class PageToSVGRegressionTests(SVGTestCase):
    def test_empty_page(self):
        page = Page()
        self.compare_page(page, "empty_page", this_path)

    def test_add_draw_object_to_page(self):
        page = Page()
        page.add_draw_object(
            TextDrawObject(
                text="some text",
                start=Position(10, 20),
                color="blue",
            )
        )

        self.compare_page(page, "add_text", this_path, tolerance=0.002)

    def test_add_line_draw_objects_to_page(self):
        page = Page()
        draw_objects = [
            HorizontalLineDrawObject(
                length=40, start=Position(10, 30), color="blue", thickness=2
            ),
            VerticalLineDrawObject(
                length=10, start=Position(10, 25), color="blue", thickness=2
            ),
            VerticalLineDrawObject(
                length=10, start=Position(50, 25), color="blue", thickness=2
            ),
        ]

        for draw_object in draw_objects:
            page.add_draw_object(draw_object)

        self.compare_page(page, "add_line_draw_objects", this_path, tolerance=0.002)
