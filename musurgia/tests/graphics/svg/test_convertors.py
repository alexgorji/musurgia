from unittest import TestCase
import xml.etree.ElementTree as ET
import svg
import subprocess
from pathlib import Path

from musurgia.graphics.svg.convertors import SVGConverterRegistry


from musurgia.graphics.drawobject import (
    Container,
    HorizontalLineDrawObject,
    LineDrawObject,
    Position,
    RectangleDrawObject,
    Size,
    TextDrawObject,
    VerticalLineDrawObject,
    create_measure_context,
)
from musurgia.graphics.svg.convertors import (
    TextDrawObjectToSVGConvertor,
)


class ConvertTextDrawObjectToSVGTestCase(TestCase):
    def test_cairo_font_extents(self):
        ctx = create_measure_context()
        ctx.select_font_face("DejaVu Sans")
        ctx.set_font_size(TextDrawObject.convert_font_size_to_mm(12))
        ext = ctx.text_extents("something")
        print(f"\nx_bearing: {ext.x_bearing}")  # should be ~-0.2294, not 0.0
        assert (
            ext.x_bearing != 0.0
        ), "cairo is using fallback font — fontconfig not applied"

    def test_dejavu_font_resolves_to_repo_font(self):
        fonts_dir = Path(__file__).parent / "fonts"
        result = subprocess.run(
            ["fc-match", "--format=%{file}", "DejaVu Sans"],
            capture_output=True,
            text=True,
        )
        assert result.stdout.strip() == str(fonts_dir / "DejaVuSans.ttf")

    def test_convertor(self):
        draw_object = TextDrawObject(text="something")
        svg_str = (
            TextDrawObjectToSVGConvertor(Position(0, 0), draw_object)
            .convert()[0]
            .as_str()
        )
        root = ET.fromstring(svg_str)
        assert round(float(root.attrib["x"]), 4) == (-0.2294)
        assert root.attrib["y"] == "3.216341145833333"
        assert root.attrib["font-family"] == draw_object.font_family
        assert round(float(root.attrib["font-size"]), 4) == 4.2333

        assert root.attrib["fill"] == draw_object.color


class ConvertDrawObjectToSVGElementTestCase(TestCase):
    def test_converts_to_element(self):
        assert isinstance(
            SVGConverterRegistry.convert(
                Position(0, 0), TextDrawObject(text="something")
            )[0],
            svg.Element,
        )

        assert isinstance(
            SVGConverterRegistry.convert(
                Position(0, 0), LineDrawObject(end=Position(30, 40))
            )[0],
            svg.Element,
        )

        assert isinstance(
            SVGConverterRegistry.convert(
                Position(0, 0), RectangleDrawObject(size=Size(20, 40))
            )[0],
            svg.Element,
        )


class ConvertBoxToSVG(TestCase):
    def test_box_is_converted(self):
        line = LineDrawObject(end=Position(30, 40))
        assert len(SVGConverterRegistry.convert(Position(0, 0), line)) == 1

        line.box.show = True
        assert len(SVGConverterRegistry.convert(Position(0, 0), line)) == 2


class ContainerTestCase(TestCase):
    def test_elements(self):
        container = Container()
        container.add_draw_object(Position(10, 10), VerticalLineDrawObject(length=5))
        container.add_draw_object(Position(10, 15), HorizontalLineDrawObject(length=20))
        container.add_draw_object(Position(10, 30), VerticalLineDrawObject(length=5))

        parent_container = Container()
        parent_container.add_draw_object(Position(30, 30), container)

        elements = SVGConverterRegistry.convert(Position(50, 50), parent_container)

        assert len(elements) == 3

        for el in elements:
            assert isinstance(el, svg.Element)
