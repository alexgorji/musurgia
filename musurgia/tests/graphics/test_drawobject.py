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

    def test_line_padding(self):
        line = LineDrawObject(end=Position(20, 30))
        assert line.padding == Padding(0, 0, 0, 0)

        line = LineDrawObject(start=Position(20, 30), end=Position(40, 60))
        assert line.padding == Padding(30, 0, 0, 20)

        line = LineDrawObject(
            start=Position(20, 30),
            end=Position(40, 60),
            right_padding=40,
            bottom_padding=50,
        )
        assert line.padding == Padding(30, 40, 50, 20)


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
    def test_line_draw_object(self):
        line = LineDrawObject(end=Position(20, 30))
        assert line.box.size == Size(20, 30)

        line = LineDrawObject(start=Position(20, 30), end=Position(40, 60))
        assert line.size == Size(20, 30)
        assert line.box.size == Size(40, 60)

        line = LineDrawObject(
            start=Position(20, 30),
            end=Position(40, 60),
            right_padding=50,
            bottom_padding=100,
        )

        assert line.box.size == Size(90, 160)

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
        assert container.size == Size(40, 43)
