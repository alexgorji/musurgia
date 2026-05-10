from unittest import TestCase

from musurgia.graphics.geometry import Position, Size
from musurgia.graphics.drawobject import (
    Line,
    Rectangle,
)


class LineTestCase(TestCase):

    def test_size(self):
        l1 = Line(start=Position(0, 40), end=Position(30, 0))
        self.assertAlmostEqual(l1.size.width, 30, delta=0.5)
        self.assertAlmostEqual(l1.size.height, 40, delta=0.5)

    def test_get_length(self):
        l1 = Line(start=Position(0, 40), end=Position(30, 0))
        assert l1.get_length() == 50

    def test_line_get_bounding_box_coordinates(self):
        l1 = Line(start=Position(0, 40), end=Position(30, 0))
        coors = l1.get_bounding_box_coordinates()
        self.assertAlmostEqual(coors.tl.x, 0, delta=0.5)
        self.assertAlmostEqual(coors.tl.y, 0, delta=0.5)
        self.assertAlmostEqual(coors.tr.x, 30, delta=0.5)
        self.assertAlmostEqual(coors.tr.y, 0, delta=0.5)
        self.assertAlmostEqual(coors.br.x, 30, delta=0.5)
        self.assertAlmostEqual(coors.br.y, 40, delta=0.5)
        self.assertAlmostEqual(coors.bl.x, 0, delta=0.5)
        self.assertAlmostEqual(coors.bl.y, 40, delta=0.5)

    def test_line_box_size(self):
        l1 = Line(start=Position(0, 40), end=Position(30, 0))
        self.assertAlmostEqual(l1.box.size.width, 30, delta=0.5)
        self.assertAlmostEqual(l1.box.size.height, 40, delta=0.5)


class RectangleTestCase(TestCase):
    def test_size(self):
        r = Rectangle(size=Size(30, 40))
        assert r.size == Size(30, 40)


class DrawObjectBoxTestCase(TestCase):
    def test_box_rectangle(self):
        line = Line(
            start=Position(20, 30),
            end=Position(40, 60),
        )
        box_rectangle = line.box.get_rectangle()
        assert isinstance(box_rectangle, Rectangle)
        assert box_rectangle.size == line.box.size
