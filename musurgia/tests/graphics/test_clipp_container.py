from unittest import TestCase

from musurgia.graphics.container import ClippingArea, Container
from musurgia.graphics.drawobject import Position, Size, StraightLineDrawObject
from musurgia.graphics.line_segment import Label
from musurgia.graphics.models import LineOrientation
from musurgia.graphics.segmented_line import SegmentedLine


class ClippingAreaTestCase(TestCase):
    def setUp(self):
        self.container = Container()
        self.line = StraightLineDrawObject(type=LineOrientation.HORIZONTAL, length=250)
        self.container.add_draw_object(Position(10, 10), self.line)

    def test_get_width(self):
        assert (
            self.container._get_clipping_area_width(start=Position(100, 0), width=100)
            == 100
        )
        assert (
            self.container._get_clipping_area_width(start=Position(200, 0), width=100)
            == 60
        )
        assert (
            self.container._get_clipping_area_width(start=Position(100, 0), width=None)
            == 160
        )

    def test_get_draw_object_is_inside_area(self):
        clipping_area = ClippingArea(start=Position(5, 5), width=500, height=500)
        assert (
            clipping_area._drawobject_is_inside_area(Position(10, 10), self.line)
            is True
        )

        clipping_area = ClippingArea(start=Position(15, 15), width=100, height=100)
        assert (
            clipping_area._drawobject_is_inside_area(Position(10, 10), self.line)
            is False
        )

        clipping_area = ClippingArea(start=Position(5, 5), width=100, height=100)
        assert (
            clipping_area._drawobject_is_inside_area(Position(10, 10), self.line)
            is False
        )

    def test_clip_all_objects_inside(self):
        lengths = [1, 1, 3.4, 5.6]
        sl = SegmentedLine(
            type=LineOrientation.HORIZONTAL,
            segment_lengths=lengths,
        )
        container = Container()
        container.add_draw_object(Position(5, 5), sl)
        ca = ClippingArea(Position(0, 0), container.size.width, container.size.height)
        assert ca._get_end() == Position(x=16, y=11.0)

        assert ca._drawobject_is_inside_area(Position(5, 5), sl) is True
        clipped = container.clip()
        assert isinstance(clipped, Container)
        assert len(clipped.get_draw_objects()) == 1
        do = clipped.get_draw_objects()[0]
        assert isinstance(do, SegmentedLine)
        assert do != sl

    def test_clip_new_position_of_inside(self):
        lengths = [1, 1, 3.4, 5.6]
        sl = SegmentedLine(
            type=LineOrientation.HORIZONTAL,
            segment_lengths=lengths,
        )
        container = Container()
        container.add_draw_object(Position(10, 10), sl)
        p, _ = container.clip(Position(4, 4)).get_draw_objects(positioned=True)[0]
        assert p == Position(6, 6)

    def test_clip_simple_line(self):
        do = StraightLineDrawObject(
            type=LineOrientation.HORIZONTAL, length=20, thickness=1
        )
        container = Container()
        position = Position(10, 9.5)
        container.add_draw_object(position, do)

        clipped = container.clip(width=25)
        assert clipped.size == Size(25, 10)
        assert isinstance(clipped, Container)
        p, cpo = clipped.get_draw_objects(positioned=True)[0]
        assert isinstance(cpo, StraightLineDrawObject)
        assert cpo != do
        assert cpo.get_length() == 25 - 10
        assert p == position


class ClipLineTestCase(TestCase):
    def test_clip_all_objects_inside(self):
        lengths = [1, 1, 3.4, 5.6]
        sl = SegmentedLine(
            type=LineOrientation.HORIZONTAL,
            segment_lengths=lengths,
            options={
                2: {"start_marker": {"labels": [Label(text="Label")]}},
            },
        )
        container = Container()
        container.add_draw_object(Position(5, 5), sl)
        clipped = container.clip()
        # assert isinstance(clipped, Container)

    def test_clip_one_horizontal_line(self):
        container = Container()
        line = StraightLineDrawObject(type=LineOrientation.HORIZONTAL, length=250)
        container.add_draw_object(Position(10, 10), line)

        clipped = [
            container.clip(width=100, start=Position(x, 0)) for x in [0, 100, 200]
        ]

        for cl in clipped:
            assert isinstance(cl, Container)
            assert cl.size.width == 100
            assert cl.size.height == container.size.height

        for cl in clipped[:2]:
            pass
