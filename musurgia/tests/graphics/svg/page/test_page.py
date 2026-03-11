from pathlib import Path
from unittest import TestCase
import pytest

from musurgia.graphics.drawobject import (
    Container,
    HorizontalLineDrawObject,
    LineDrawObject,
    Padding,
    Position,
    RectangleDrawObject,
    Size,
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
        page.add_draw_object(Position(0, 0), TextDrawObject(text="some text"))
        assert "some text" in page.convert_to_svg_string()

    def test_add_multiple_draw_objects_to_page(self):
        page = Page()
        page.add_draw_object(
            Position(0, 0), TextDrawObject(text="Hello", start=Position(10, 10))
        )

        page.add_draw_object(
            Position(0, 0), TextDrawObject(text="Goodbye", start=Position(20, 20))
        )

        svg_string = page.convert_to_svg_string()
        assert "Hello" in svg_string
        assert "Goodbye" in svg_string


class PageToSVGRegressionTests(SVGTestCase):
    def test_empty_page(self):
        page = Page()
        self.compare_page(page, "empty_page", this_path)

    @pytest.mark.nonci
    def test_add_text_draw_object_to_page(self):
        page = Page()
        t1 = TextDrawObject(
            text="The quick Brown fox Jumps over The lazy Dog",
            color="blue",
            font_size=12,
        )

        t1.box.show = True
        page.add_draw_object(Position(30, 50), t1)

        t2 = TextDrawObject(
            text="The quick Brown fox Jumps over The lazy Dog",
            color="red",
            start=Position(10, 20),
            font_size=12,
        )
        t2.box.show = True
        page.add_draw_object(Position(30, 100), t2)

        t3 = TextDrawObject(
            text="The quick Brown fox Jumps over The lazy Dog",
            color="orange",
            start=Position(10, 20),
            font_size=15,
            right_padding=30,
            bottom_padding=40,
        )
        t3.box.show = True
        page.add_draw_object(Position(30, 180), t3)

        self.compare_page(
            page, "add_text_draw_object", this_path, width=210 * 2, height=297 * 2
        )

    def test_add_line_draw_object_to_page(self):
        page = Page()

        l1 = LineDrawObject(end=Position(30, 40), color="blue", thickness=2)
        l1.box.show = True
        page.add_draw_object(Position(30, 30), l1)

        l2 = HorizontalLineDrawObject(length=20, color="gray", thickness=2)
        l2.box.show = True
        page.add_draw_object(Position(30, 100), l2)

        l3 = VerticalLineDrawObject(length=20, color="gray", thickness=2)
        l3.box.show = True
        page.add_draw_object(Position(30, 150), l3)

        l4 = LineDrawObject(
            start=Position(0, 40), end=Position(30, 0), color="orange", thickness=2
        )
        l4.box.show = True
        page.add_draw_object(Position(130, 30), l4)

        self.compare_page(
            page, "add_line_draw_objects", this_path, width=210, height=297
        )

    def test_add_multiple_line_draw_objects_to_page(self):
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
            page.add_draw_object(Position(0, 0), draw_object)

        self.compare_page(
            page, "add_multiple_line_draw_objects", this_path, width=210, height=297
        )

    def test_add_nested_container_to_page(self):
        container = Container()
        container.add_draw_object(Position(10, 10), VerticalLineDrawObject(length=10))
        container.add_draw_object(Position(10, 15), HorizontalLineDrawObject(length=30))
        container.add_draw_object(Position(40, 10), VerticalLineDrawObject(length=10))
        for _, draw_object in container.get_draw_objects():
            if isinstance(draw_object, LineDrawObject):
                draw_object.set_color("blue")
                draw_object.set_thickness(1)

        parent_container = Container()
        parent_container.add_draw_object(Position(30, 30), container)

        page = Page()
        page.add_draw_object(Position(50, 50), parent_container)

        self.compare_page(
            page, "add_nested_container", this_path, width=210, height=297
        )

    def test_add_rectangle(self):
        page = Page()
        r = RectangleDrawObject(size=Size(30, 40), color="blue", thickness=1)
        page.add_draw_object(Position(10, 10), r)

        self.compare_page(page, "add_rectangle", this_path, width=210, height=297)

    def test_boxed_rectangle(self):
        page = Page()
        r1 = RectangleDrawObject(size=Size(30, 40), color="blue", thickness=5)

        r2 = RectangleDrawObject(
            size=Size(30, 40),
            color="blue",
            thickness=1,
            padding=Padding(10, 20, 30, 40),
        )
        r1.box.show = True
        r2.box.show = True

        page.add_draw_object(Position(50, 50), r1)
        page.add_draw_object(Position(50, 150), r2)

        self.compare_page(
            page, "boxed_rectangle", this_path, width=210 * 2, height=297 * 2
        )

    @pytest.mark.nonci
    def test_add_container(self):
        page = Page()
        container = Container()

        l1 = LineDrawObject(end=Position(20, 40), color="blue", thickness=2)
        l2 = LineDrawObject(
            start=Position(0, 40), end=Position(20, 0), color="orange", thickness=2
        )

        r1 = RectangleDrawObject(
            size=Size(30, 40),
            color="blue",
            thickness=1,
            padding=Padding(2, 4, 6, 8),
        )

        t1 = TextDrawObject(
            text="I am in a container",
            color="red",
            font_size=12,
        )

        positions = [
            Position(0, 0),
            Position(0, 50),
            Position(0, 100),
            Position(60, 150),
        ]
        for p, o in zip(positions, [l1, r1, t1, l2]):
            o.box.show = True
            container.add_draw_object(p, o)

        container.box.show = True
        print(container.get_bounding_box_coordinates())
        page.add_draw_object(Position(10, 10), container)

        self.compare_page(
            page, "add_container", this_path, width=210 * 2, height=297 * 2
        )
