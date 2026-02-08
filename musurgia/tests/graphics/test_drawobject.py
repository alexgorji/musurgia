from unittest import TestCase
from musurgia.graphics.drawobject import (
    # DrawObjectBox,
    Container,
    HorizontalLineDrawObject,
    LineDrawObject,
    Position,
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


class TextDrawObjectTestCase(TestCase):

    def test_text_measure(self):
        t = TextDrawObject(text="Hello World")
        size = t.measure()
        assert size.width > 0
        assert size.height > 0
        size2 = t.measure()
        assert size == size2, f"Repeated measurement must be identical for {t.text}"


class DrawObjectBoxTestCase(TestCase):
    def test_line_draw_object(self):
        line = LineDrawObject(end=Position(20, 30))
        assert line.box.get_size() == Size(20, 30)


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
