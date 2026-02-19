from unittest import TestCase

from musurgia.graphics.drawobject import (
    Container,
    HorizontalLineDrawObject,
    Size,
    TextDrawObject,
    VerticalLineDrawObject,
    Position,
)


class ContainerTestCase(TestCase):
    def test_size(self):
        hl = HorizontalLineDrawObject(length=20, thickness=1)
        marker_1 = VerticalLineDrawObject(length=6, thickness=1)
        marker_2 = VerticalLineDrawObject(length=6, thickness=1)
        container = Container()
        container.add_draw_object(Position(20, 40), hl).add_draw_object(
            Position(20, 37), marker_1
        ).add_draw_object(Position(40, 37), marker_2)
        assert container.size == Size(40.5, 43)

    def test_color(self):
        with self.assertRaises(TypeError):
            Container(color="blue")

    def test_containers_get_draw_objects_recursive(self):
        start_marker = VerticalLineDrawObject(length=6, thickness=1)
        end_marker = VerticalLineDrawObject(length=6, thickness=1)
        straight_line = HorizontalLineDrawObject(length=20, thickness=1)

        start_marker_p = Position(100, 110)
        straight_line_p = Position(100, 113)
        end_marker_p = Position(120, 110)

        line_segment = Container()

        line_segment.add_draw_object(start_marker_p, start_marker).add_draw_object(
            straight_line_p, straight_line
        ).add_draw_object(end_marker_p, end_marker)

        assert (
            {(p, o) for p, o in line_segment.get_draw_objects(recursive=True)}
            == {(p, o) for p, o in line_segment.get_draw_objects(recursive=False)}
            == {
                (start_marker_p, start_marker),
                (straight_line_p, straight_line),
                (end_marker_p, end_marker),
            }
        )

    def test_nested_containers_get_draw_objects_recursive(self):
        start_marker = VerticalLineDrawObject(length=6, thickness=1)
        start_marker_label = TextDrawObject(text="label")
        start_marker_p = Position(0, 10)
        start_marker_label_p = Position(0, 0)

        labeled_start_marker = Container()
        labeled_start_marker.add_draw_object(
            start_marker_p, start_marker
        ).add_draw_object(start_marker_label_p, start_marker_label)
        end_marker = VerticalLineDrawObject(length=6, thickness=1)
        straight_line = HorizontalLineDrawObject(length=20, thickness=1)

        labeled_start_marker_p = Position(100, 100)
        straight_line_p = Position(100, 113)
        end_marker_p = Position(120, 110)

        line_segment = Container()
        line_segment.add_draw_object(labeled_start_marker_p, labeled_start_marker)
        line_segment.add_draw_object(straight_line_p, straight_line).add_draw_object(
            end_marker_p, end_marker
        )

        assert {(p, o) for p, o in line_segment.get_draw_objects()} == {
            (labeled_start_marker_p, labeled_start_marker),
            (straight_line_p, straight_line),
            (end_marker_p, end_marker),
        }

        assert {(p, o) for p, o in line_segment.get_draw_objects(recursive=True)} == {
            (start_marker_p + labeled_start_marker_p, start_marker),
            (start_marker_label_p + labeled_start_marker_p, start_marker_label),
            (straight_line_p, straight_line),
            (end_marker_p, end_marker),
        }
