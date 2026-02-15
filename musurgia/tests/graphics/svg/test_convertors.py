from unittest import TestCase
import xml.etree.ElementTree as ET
import svg

from musurgia.graphics.drawobject import (
    LineDrawObject,
    Position,
    RectangleDrawObject,
    Size,
    TextDrawObject,
)
from musurgia.graphics.svg.convertors import (
    SVGConverterRegistry,
    TextDrawObjectToSVGConvertor,
)


class ConvertTextDrawObjectToSVGTestCase(TestCase):
    def test_convertor(self):
        draw_object = TextDrawObject(text="something")
        svg_str = (
            TextDrawObjectToSVGConvertor(Position(0, 0), draw_object)
            .convert()[0]
            .as_str()
        )
        root = ET.fromstring(svg_str)
        assert root.attrib["x"] == "0"
        assert root.attrib["y"] == "3.0468424479166663"
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
