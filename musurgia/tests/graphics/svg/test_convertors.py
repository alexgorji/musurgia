from unittest import TestCase
import xml.etree.ElementTree as ET

from musurgia.graphics.drawobject import TextDrawObject
from musurgia.graphics.svg.convertors import ConvertTextDrawObjectToSVG


class ConvertTextDrawObjectToSVGTestCase(TestCase):
    def test_convertor(self):
        draw_object = TextDrawObject(text="something")
        svg_str = ConvertTextDrawObjectToSVG(draw_object).convert().as_str()
        root = ET.fromstring(svg_str)
        assert root.attrib["x"] == "0"
        assert root.attrib["y"] == "0"
        assert root.attrib["font-family"] == draw_object.font_family
        assert round(float(root.attrib["font-size"]), 4) == 4.2333

        assert root.attrib["fill"] == draw_object.color
