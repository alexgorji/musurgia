from pathlib import Path
from unittest import TestCase
import pytest

from musurgia.graphics.container import Container
from musurgia.graphics.geometry import Paddings, Position, Size
from musurgia.graphics.drawobject import (
    Line,
    LineOptions,
    RectangleDrawObject,
    StraightLine,
    Text,
    TextOptions,
)
from musurgia.graphics.geometry import LineOrientation
from musurgia.graphics.svg.paginator import SVGPage
from musurgia.tests.helpers.svg import SVGTestCase
import xml.etree.ElementTree as ET

this_path = Path(__file__)


class PageToSVGTestCase(TestCase):
    def test_empty_page_to_svg(self):
        page = SVGPage()
        svg_xml = page.as_svg().as_str()
        root = ET.fromstring(svg_xml)
        assert root.attrib["width"] == "210mm"
        assert root.attrib["height"] == "297mm"
        assert root.attrib["viewBox"] == "0 0 210 297"

    def test_add_text_to_page(self):
        page = SVGPage()
        page.add_draw_object(Position(0, 0), Text(text="some text"))
        assert "some text" in page.convert_to_svg_string()

    def test_add_multiple_draw_objects_to_page(self):
        page = SVGPage()
        page.add_draw_object(
            Position(0, 0),
            Text(text="Hello", padding=Paddings(10, 0, 0, 10)),
        )

        page.add_draw_object(
            Position(0, 0),
            Text(text="Goodbye", padding=Paddings(20, 0, 0, 20)),
        )

        svg_string = page.convert_to_svg_string()
        assert "Hello" in svg_string
        assert "Goodbye" in svg_string


class PageToSVGRegressionTests(SVGTestCase):
    def test_empty_page(self):
        page = SVGPage()
        self.compare_page(page, "empty_page", this_path)

    def test_empty_page_with_grid(self):
        page = SVGPage()
        page.add_grid()
        self.compare_page(page, "empty_page_with_grid", this_path)

    def test_add_line_draw_object_to_page(self):
        page = SVGPage()
        page.add_background("white")
        l1 = Line(end=Position(30, 40), options=LineOptions(color="blue", thickness=2))
        l1.box.show = True
        page.add_draw_object(Position(30, 30), l1)

        l2 = StraightLine(
            type=LineOrientation.HORIZONTAL,
            length=20,
            options=LineOptions(color="gray", thickness=2),
        )
        l2.box.show = True
        page.add_draw_object(Position(30, 100), l2)

        l3 = StraightLine(
            type=LineOrientation.VERTICAL,
            length=20,
            options=LineOptions(color="gray", thickness=2),
        )
        l3.box.show = True
        page.add_draw_object(Position(30, 150), l3)

        l4 = Line(
            start=Position(0, 40),
            end=Position(30, 0),
            options=LineOptions(color="orange", thickness=2),
        )
        l4.box.show = True
        page.add_draw_object(Position(130, 30), l4)

        self.compare_page(
            page, "add_line_draw_objects", this_path, width=210, height=297
        )

    def test_add_multiple_line_draw_objects_to_page(self):
        page = SVGPage()
        draw_objects = [
            StraightLine(
                type=LineOrientation.HORIZONTAL,
                length=40,
                options=LineOptions(thickness=2),
            ),
            StraightLine(
                type=LineOrientation.VERTICAL,
                length=10,
                options=LineOptions(thickness=2),
            ),
            StraightLine(
                type=LineOrientation.VERTICAL,
                length=10,
                options=LineOptions(thickness=2),
            ),
        ]
        positions = [Position(10, 30), Position(10, 25), Position(50, 25)]
        for position, draw_object in zip(positions, draw_objects, strict=True):
            page.add_draw_object(position, draw_object)

        self.compare_page(
            page, "add_multiple_line_draw_objects", this_path, width=210, height=297
        )

    def test_add_nested_container_to_page(self):
        container = Container()
        container.add_draw_object(
            Position(10, 10),
            StraightLine(type=LineOrientation.VERTICAL, length=10),
        )
        container.add_draw_object(
            Position(10, 15),
            StraightLine(type=LineOrientation.HORIZONTAL, length=30),
        )
        container.add_draw_object(
            Position(40, 10),
            StraightLine(type=LineOrientation.VERTICAL, length=10),
        )
        for _, draw_object in container.get_draw_objects(positioned=True):
            if isinstance(draw_object, Line):
                draw_object.set_color("blue")
                draw_object.set_thickness(1)

        parent_container = Container()
        parent_container.add_draw_object(Position(30, 30), container)

        page = SVGPage()
        page.add_draw_object(Position(50, 50), parent_container)

        self.compare_page(
            page, "add_nested_container", this_path, width=210, height=297
        )

    def test_add_rectangle(self):
        page = SVGPage()
        r = RectangleDrawObject(size=Size(30, 40), color="blue", thickness=1)
        page.add_draw_object(Position(10, 10), r)

        self.compare_page(page, "add_rectangle", this_path, width=210, height=297)

    def test_boxed_rectangle(self):
        page = SVGPage()
        r1 = RectangleDrawObject(size=Size(30, 40), color="blue", thickness=5)

        r2 = RectangleDrawObject(
            size=Size(30, 40),
            color="blue",
            thickness=1,
            padding=Paddings(10, 20, 30, 40),
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
        page = SVGPage()
        container = Container()

        l1 = Line(end=Position(20, 40), options=LineOptions(color="blue", thickness=2))
        l2 = Line(
            start=Position(0, 40),
            end=Position(20, 0),
            options=LineOptions(color="orange", thickness=2),
        )

        r1 = RectangleDrawObject(
            size=Size(30, 40),
            color="blue",
            thickness=1,
            padding=Paddings(2, 4, 6, 8),
        )

        t1 = Text(text="I am in a container", options=TextOptions(color="red"))

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
        page.add_draw_object(Position(10, 10), container)

        self.compare_page(
            page, "add_container", this_path, width=210 * 2, height=297 * 2
        )
