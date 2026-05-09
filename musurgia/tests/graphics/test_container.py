from unittest import TestCase


from musurgia.graphics.container import Container
from musurgia.graphics.geometry import Position, Size
from musurgia.graphics.drawobject import (
    StraightLineDrawObject,
    TextDrawObject,
)
from musurgia.graphics.geometry import LineOrientation


class ContainerTestCase(TestCase):
    def test_size(self):
        hl = StraightLineDrawObject(
            type=LineOrientation.HORIZONTAL, length=20, thickness=1
        )
        marker_1 = StraightLineDrawObject(
            type=LineOrientation.VERTICAL, length=6, thickness=1
        )
        marker_2 = StraightLineDrawObject(
            type=LineOrientation.VERTICAL, length=6, thickness=1
        )
        container = Container()
        container.add_draw_object(Position(20, 40), hl).add_draw_object(
            Position(20, 37), marker_1
        ).add_draw_object(Position(40, 37), marker_2)
        assert container.size == Size(40.5, 43)

    def test_color(self):
        with self.assertRaises(TypeError):
            Container(color="blue")

    def _create_test_containers(self):
        start_marker = StraightLineDrawObject(
            type=LineOrientation.VERTICAL, length=6, thickness=1
        )
        end_marker = StraightLineDrawObject(
            type=LineOrientation.VERTICAL, length=6, thickness=1
        )
        straight_line = StraightLineDrawObject(
            type=LineOrientation.HORIZONTAL, length=20, thickness=1
        )

        start_marker_p = Position(100, 110)
        straight_line_p = Position(100, 113)
        end_marker_p = Position(120, 110)

        line_segment = Container()

        line_segment.add_draw_object(start_marker_p, start_marker).add_draw_object(
            straight_line_p, straight_line
        ).add_draw_object(end_marker_p, end_marker)

        return [
            line_segment,
            start_marker_p,
            start_marker,
            straight_line_p,
            straight_line,
            end_marker_p,
            end_marker,
        ]

    def test_containers_get_positioned_draw_objects_recursive(self):
        [
            line_segment,
            start_marker_p,
            start_marker,
            straight_line_p,
            straight_line,
            end_marker_p,
            end_marker,
        ] = self._create_test_containers()
        dos = line_segment.get_draw_objects(positioned=True, recursive=False)
        rdos = line_segment.get_draw_objects(positioned=True, recursive=True)
        assert len(dos) == len(rdos) == 3

        assert (start_marker_p, start_marker) in dos
        assert (straight_line_p, straight_line) in dos
        assert (end_marker_p, end_marker) in dos

        assert (start_marker_p, start_marker) in rdos
        assert (straight_line_p, straight_line) in rdos
        assert (end_marker_p, end_marker) in rdos

    def test_containers_get_draw_objects_recursive(self):
        [
            line_segment,
            _,
            start_marker,
            _,
            straight_line,
            _,
            end_marker,
        ] = self._create_test_containers()

        assert (
            line_segment.get_draw_objects(recursive=True)
            == line_segment.get_draw_objects(recursive=False)
            == [start_marker, straight_line, end_marker]
        )

    def _create_test_nested_containers(self):
        start_marker = StraightLineDrawObject(
            type=LineOrientation.VERTICAL, length=6, thickness=1
        )
        start_marker_label = TextDrawObject(text="label")
        start_marker_p = Position(0, 10)
        start_marker_label_p = Position(0, 0)

        labeled_start_marker = Container()
        labeled_start_marker.add_draw_object(
            start_marker_p, start_marker
        ).add_draw_object(start_marker_label_p, start_marker_label)
        end_marker = StraightLineDrawObject(
            type=LineOrientation.VERTICAL, length=6, thickness=1
        )
        straight_line = StraightLineDrawObject(
            type=LineOrientation.HORIZONTAL, length=20, thickness=1
        )

        labeled_start_marker_p = Position(100, 100)
        straight_line_p = Position(100, 113)
        end_marker_p = Position(120, 110)

        line_segment = Container()
        line_segment.add_draw_object(labeled_start_marker_p, labeled_start_marker)
        line_segment.add_draw_object(straight_line_p, straight_line).add_draw_object(
            end_marker_p, end_marker
        )
        return [
            line_segment,
            labeled_start_marker_p,
            labeled_start_marker,
            straight_line_p,
            straight_line,
            start_marker_p,
            start_marker,
            start_marker_label_p,
            start_marker_label,
            end_marker_p,
            end_marker,
        ]

    def test_nested_containers_get_positioned_draw_objects_recursive(self):
        [
            line_segment,
            labeled_start_marker_p,
            labeled_start_marker,
            straight_line_p,
            straight_line,
            start_marker_p,
            start_marker,
            start_marker_label_p,
            start_marker_label,
            end_marker_p,
            end_marker,
        ] = self._create_test_nested_containers()

        pdos = line_segment.get_draw_objects(positioned=True)
        assert (labeled_start_marker_p, labeled_start_marker) in pdos
        assert (straight_line_p, straight_line) in pdos
        assert (end_marker_p, end_marker) in pdos

        pdos = line_segment.get_draw_objects(positioned=True, recursive=True)
        assert (start_marker_p + labeled_start_marker_p, start_marker) in pdos
        assert (
            start_marker_label_p + labeled_start_marker_p,
            start_marker_label,
        ) in pdos
        assert (straight_line_p, straight_line) in pdos
        assert (end_marker_p, end_marker) in pdos

    def test_nested_containers_get_draw_objects_recursive(self):

        [
            line_segment,
            _,
            labeled_start_marker,
            _,
            straight_line,
            _,
            start_marker,
            _,
            start_marker_label,
            _,
            end_marker,
        ] = self._create_test_nested_containers()
        dos = line_segment.get_draw_objects()
        assert labeled_start_marker in dos
        assert straight_line in dos
        assert end_marker in dos

        dos = line_segment.get_draw_objects(recursive=True)
        assert start_marker in dos
        assert start_marker_label in dos
        assert straight_line in dos
        assert end_marker in dos

    def test_empty_container(self):
        empty_container = Container()
        assert empty_container.get_draw_objects() == []
        assert empty_container.get_draw_objects(positioned=True) == []
