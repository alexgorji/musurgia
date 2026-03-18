from unittest import TestCase

from musurgia.graphics.drawobject import Position, TextDrawObject
from musurgia.graphics.models import LineOrientation
from musurgia.graphics.segmented_line import SegmentedLine


class HorizontalSegmentedLineTestCase(TestCase):
    def setUp(self) -> None:
        self.lengths = [1, 2, 3.4, 5.6]
        self.sl = SegmentedLine(
            type=LineOrientation.HORIZONTAL, segment_lengths=self.lengths
        )

    def test_init(self):
        sl = SegmentedLine(type=LineOrientation.HORIZONTAL)
        assert sl.type.value == "horizontal"
        assert sl.get_draw_objects() == []

    def test_segmented_lines_with_lengths(self):
        dos = self.sl.get_draw_objects()
        assert len(dos) == 4
        assert self.sl.get_length() == sum(self.lengths)

    def test_get_line_segments(self):
        self.sl.add_draw_object(Position(10, 10), TextDrawObject(text="dummy"))
        lss = self.sl.get_line_segments()
        assert len(lss) == 4

    def test_get_positioned_line_segments(self):
        self.sl.add_draw_object(Position(10, 10), TextDrawObject(text="dummy"))
        plss = self.sl.get_positioned_line_segments()
        assert len(plss) == 4

    def test_default_marker_values(self):
        lss = self.sl.get_line_segments()
        for ls in lss:
            start, end = ls.get_markers()
            assert start.get_length() == 6
            assert end.get_length() == 6
            assert start.get_color() == "black"
            assert end.get_color() == "black"
            assert start.show is True
            if ls != lss[-1]:
                assert end.show is False
            else:
                assert end.show is True

    def test_setting_marker_length(self):
        sl = SegmentedLine(
            type=LineOrientation.HORIZONTAL,
            segment_lengths=self.lengths,
            marker_length=100,
        )
        for ls in sl.get_line_segments():
            start, end = ls.get_markers()
            assert start.get_length() == 100
            assert end.get_length() == 100

    def test_aligned_segmented_lines(self):
        lengths = [1, 2, 3.4, 5.6]
        sl = SegmentedLine(type=LineOrientation.HORIZONTAL, segment_lengths=lengths)
        lss = sl.get_positioned_line_segments()
        first_straight_line_y_position = lss[0][0].y
        for ls in lss[1:]:
            assert ls[0].y == first_straight_line_y_position
