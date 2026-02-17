from unittest import TestCase

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


class LineDrawObjectTestCase(TestCase):

    def test_horizontal_line(self):
        hl = HorizontalLineDrawObject(start=Position(20, 40), length=10)
        assert hl.end.x, hl.end.y == (30, 40)

    def test_vertical_line(self):
        hl = VerticalLineDrawObject(start=Position(20, 30), length=10)
        assert hl.end.x, hl.end.y == (20, 40)

    def test_default_line_padding(self):
        line = LineDrawObject(end=Position(30, 40))
        assert line.padding == Padding(0, 0, 0, 0)

        line = LineDrawObject(start=Position(0, 40), end=Position(30, 0))
        assert line.padding == Padding(0, 0, 0, 0)

        line = LineDrawObject(start=Position(30, 40), end=Position(0, 0))
        assert line.padding == Padding(0, 0, 0, 0)

        line = LineDrawObject(start=Position(30, 0), end=Position(0, 40))
        assert line.padding == Padding(0, 0, 0, 0)

    def test_line_padding(self):
        line = LineDrawObject(start=Position(20, 30), end=Position(40, 60))
        assert line.padding == Padding(30, 0, 0, 20)

        line = LineDrawObject(
            start=Position(20, 30),
            end=Position(40, 60),
            right_padding=40,
            bottom_padding=50,
        )
        assert line.padding == Padding(30, 40, 50, 20)

    def test_horizontal_line_size(self):
        hl = HorizontalLineDrawObject(length=10, thickness=2)
        assert hl.size == Size(10, 2)

    def test_vertical_line_size(self):
        vl = VerticalLineDrawObject(length=10, thickness=2)
        assert vl.size == Size(2, 10)

    def test_line_size(self):
        l1 = LineDrawObject(start=Position(0, 40), end=Position(30, 0))
        self.assertAlmostEqual(l1.size.width, 30, delta=0.5)
        self.assertAlmostEqual(l1.size.height, 40, delta=0.5)

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

    def test_get_length(self):
        l1 = LineDrawObject(start=Position(0, 40), end=Position(30, 0))
        assert l1.get_length() == 50

        vl = VerticalLineDrawObject(length=10, thickness=2)
        assert vl.get_length() == 10


class TextDrawObjectTestCase(TestCase):

    def test_text_size(self):
        t = TextDrawObject(text="Hello World")
        size = t.size
        assert size.width > 0
        assert size.height > 0
        size2 = t.size
        assert size == size2, f"Repeated measurement must be identical for {t.text}"


class RectangleDrawObjectTestCase(TestCase):
    def test_rectangle_size(self):
        r = RectangleDrawObject(size=Size(30, 40))
        assert r.size == Size(30, 40)


class DrawObjectBoxTestCase(TestCase):

    def test_box_rectangle(self):
        line = LineDrawObject(
            start=Position(20, 30),
            end=Position(40, 60),
            right_padding=50,
            bottom_padding=100,
        )
        box_rectangle = line.box.get_rectangle()
        assert isinstance(box_rectangle, RectangleDrawObject)
        assert box_rectangle.size == line.box.size


class ContainerTestCase(TestCase):
    def test_container_size(self):
        hl = HorizontalLineDrawObject(length=20, thickness=1)
        marker_1 = VerticalLineDrawObject(length=6, thickness=1)
        marker_2 = VerticalLineDrawObject(length=6, thickness=1)
        container = Container()
        container.add_draw_object(Position(20, 40), hl).add_draw_object(
            Position(20, 37), marker_1
        ).add_draw_object(Position(40, 37), marker_2)
        assert container.size == Size(40.5, 43)
