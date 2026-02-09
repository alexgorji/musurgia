from unittest import TestCase

from musurgia.graphics.drawobject import (
    Container,
    HorizontalLineDrawObject,
    VerticalLineDrawObject,
    Position,
)

import svg

from musurgia.graphics.svg.convertors import SVGConverterRegistry


class ContainerTestCase(TestCase):
    def test_get_relative_positions(self):
        container = Container()
        container.add_draw_object(Position(10, 10), VerticalLineDrawObject(length=5))
        container.add_draw_object(Position(10, 15), HorizontalLineDrawObject(length=20))
        container.add_draw_object(Position(10, 30), VerticalLineDrawObject(length=5))

        parent_container = Container()
        parent_container.add_draw_object(Position(30, 30), container)

        elements = SVGConverterRegistry.convert(Position(50, 50), parent_container)

        for el in elements:
            assert isinstance(el, svg.Element)
