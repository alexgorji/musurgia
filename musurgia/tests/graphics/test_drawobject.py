from unittest import TestCase

from musurgia.graphics.geometry import Position, Size
from musurgia.graphics.drawobject import (
    LineDrawObject,
    RectangleDrawObject,
    OldStraightLineDrawObject,
)
from musurgia.graphics.geometry import LineOrientation


class LineTestCase(TestCase):

    def test_size(self):
        l1 = LineDrawObject(start=Position(0, 40), end=Position(30, 0))
        self.assertAlmostEqual(l1.size.width, 30, delta=0.5)
        self.assertAlmostEqual(l1.size.height, 40, delta=0.5)

    def test_color(self):
        assert LineDrawObject(end=Position(10, 20), color="blue").color == "blue"

    def test_get_length(self):
        l1 = LineDrawObject(start=Position(0, 40), end=Position(30, 0))
        assert l1.get_length() == 50

    def test_line_get_bounding_box_coordinates(self):
        l1 = LineDrawObject(start=Position(0, 40), end=Position(30, 0))
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
        l1 = LineDrawObject(start=Position(0, 40), end=Position(30, 0))
        self.assertAlmostEqual(l1.box.size.width, 30, delta=0.5)
        self.assertAlmostEqual(l1.box.size.height, 40, delta=0.5)


class HorizontalLineTestCase(TestCase):

    def test_horizontal_line(self):
        hl = OldStraightLineDrawObject(
            type=LineOrientation.HORIZONTAL, start=Position(20, 40), length=10
        )
        assert (hl.end.x, hl.end.y) == (30, 40)

    def test_size(self):
        hl = OldStraightLineDrawObject(
            type=LineOrientation.HORIZONTAL, length=10, thickness=2
        )
        assert hl.size == Size(10, 2)

    def test_color(self):
        assert (
            OldStraightLineDrawObject(
                type=LineOrientation.HORIZONTAL, length=20, color="blue"
            ).color
            == "blue"
        )

    def test_get_length(self):
        vl = OldStraightLineDrawObject(
            type=LineOrientation.HORIZONTAL, length=10, thickness=2
        )
        assert vl.get_length() == 10


class VerticalLineTestCase(TestCase):

    def test_vertical_line(self):
        vl = OldStraightLineDrawObject(
            type=LineOrientation.VERTICAL, start=Position(20, 30), length=10
        )
        assert (vl.end.x, vl.end.y) == (20, 40)

    def test_size(self):
        vl = OldStraightLineDrawObject(
            type=LineOrientation.VERTICAL, length=10, thickness=2
        )
        assert vl.size == Size(2, 10)

    def test_color(self):
        assert (
            OldStraightLineDrawObject(
                type=LineOrientation.VERTICAL, length=20, color="blue"
            ).color
            == "blue"
        )

    def test_get_length(self):
        vl = OldStraightLineDrawObject(
            type=LineOrientation.VERTICAL, length=10, thickness=2
        )
        assert vl.get_length() == 10


class RectangleTestCase(TestCase):
    def test_size(self):
        r = RectangleDrawObject(size=Size(30, 40))
        assert r.size == Size(30, 40)

    def test_color(self):
        assert RectangleDrawObject(size=Size(10, 20), color="blue").color == "blue"


class DrawObjectBoxTestCase(TestCase):
    def test_box_rectangle(self):
        line = LineDrawObject(
            start=Position(20, 30),
            end=Position(40, 60),
        )
        box_rectangle = line.box.get_rectangle()
        assert isinstance(box_rectangle, RectangleDrawObject)
        assert box_rectangle.size == line.box.size
