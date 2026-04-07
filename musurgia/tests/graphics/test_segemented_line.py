from unittest import TestCase

from musurgia.graphics.geometry import Position
from musurgia.graphics.drawobject import TextDrawObject
from musurgia.graphics.line_segment import Label, Marker
from musurgia.graphics.geometry import LineOrientation
from musurgia.graphics.segmented_line import SegmentedLine
from musurgia.tests.graphics.test_utils import (
    check_all_straight_lines_centered,
    check_straight_line_alignment,
)


class HorizontalSegmentedLineTestCase(TestCase):
    def setUp(self) -> None:
        self.lengths = [1, 1, 3.4, 5.6]
        self.sl = SegmentedLine(
            type=LineOrientation.HORIZONTAL, segment_lengths=self.lengths
        )

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
        plss = self.sl.get_line_segments(positioned=True)
        assert len(plss) == 4

    def test_end_markers(self):
        lss = self.sl.get_line_segments()
        for ls in lss[:-1]:
            assert ls.get_markers()[1] is None
        assert lss[-1].get_markers()[1] is not None

    def test_default_marker_values(self):
        lss = self.sl.get_line_segments()
        for ls in lss:
            start, end = ls.get_markers()
            assert isinstance(start, Marker)
            assert start.get_length() == 6
            assert start.get_color() == "black"
            assert start.show is True

            if ls != lss[-1]:
                assert end is None
            else:
                assert isinstance(end, Marker)
                assert end.get_length() == 6
                assert end.get_color() == "black"

        lengths: list[int | float] = [10, 20, 34, 56]
        sl = SegmentedLine(
            type=LineOrientation.HORIZONTAL,
            segment_lengths=lengths,
            marker_length=10,
            show_last_end_marker=True,
            thickness=3,
            color="blue",
            options={
                2: {"start_marker": {"length": 20}},
            },
        )
        end_marker = sl.get_line_segments()[-1].get_markers()[1]
        assert end_marker is not None
        assert end_marker.show is True
        assert end_marker.get_color() == "blue"

    def test_setting_default_marker_length(self):
        sl = SegmentedLine(
            type=LineOrientation.HORIZONTAL,
            segment_lengths=self.lengths,
            marker_length=100,
        )
        for ls in sl.get_line_segments():
            start, end = ls.get_markers()
            assert start.get_length() == 100
            if end:
                assert end.get_length() == 100

    def test_aligned_segmented_lines(self):
        lengths = [1, 2, 3.4, 5.6]
        sl = SegmentedLine(type=LineOrientation.HORIZONTAL, segment_lengths=lengths)
        check_straight_line_alignment(sl)
        check_all_straight_lines_centered(sl)

    def test_different_marker_lengths(self):
        sl = SegmentedLine(
            type=LineOrientation.HORIZONTAL,
            segment_lengths=self.lengths,
            marker_length=100,
            options={2: {"start_marker": {"length": 10}}},
        )
        for index, ls in enumerate(sl.get_line_segments()):
            if index == 1:
                assert ls.get_markers()[0].get_length() == 10
            else:
                assert ls.get_markers()[0].get_length() == 100
        check_all_straight_lines_centered(sl)
        check_straight_line_alignment(sl)

    def test_color(self):
        sl = SegmentedLine(
            type=LineOrientation.HORIZONTAL, segment_lengths=self.lengths, color="blue"
        )

        assert {do.get_color() for do in sl.get_draw_objects(recursive=True)} == {
            "blue"
        }

        sl = SegmentedLine(
            type=LineOrientation.HORIZONTAL,
            segment_lengths=self.lengths,
            color="blue",
            options={2: {"start_marker": {"color": "red"}}},
        )

        for index, sl in enumerate(sl.get_line_segments()):
            if index == 1:
                assert sl.get_markers()[0].get_color() == "red"
            else:
                assert sl.get_markers()[0].get_color() == "blue"

    def test_thickness(self):
        sl = SegmentedLine(
            type=LineOrientation.HORIZONTAL, segment_lengths=self.lengths, thickness=5
        )

        for ls in sl.get_line_segments():
            assert ls.get_straight_line().thickness == 5
            start, end = ls.get_markers()
            assert start.get_thickness() == 5
            if end:
                assert end.get_thickness() == 5

        sl = SegmentedLine(
            type=LineOrientation.HORIZONTAL,
            segment_lengths=self.lengths,
            thickness=5,
            options={2: {"start_marker": {"thickness": 2}}},
        )

        for index, ls in enumerate(sl.get_line_segments()):
            assert ls.get_straight_line().thickness == 5
            start, end = ls.get_markers()
            expected = 2 if index == 1 else 5
            assert start.get_thickness() == expected
            if end:
                assert end.get_thickness() == 5

    def test_add_labels(self):
        labels_1 = [
            Label(text="First first layer", offset=(0, 20)),
            Label(text="First second layer", offset=(0, 10)),
        ]
        labels_2 = [
            Label(text="Second first layer", offset=(0, 5)),
            Label(text="Second second layer", offset=(0, 2)),
            Label(text="Second third layer"),
        ]

        sl = SegmentedLine(
            type=LineOrientation.HORIZONTAL,
            segment_lengths=self.lengths,
            thickness=5,
            options={
                2: {"start_marker": {"labels": labels_1}},
                4: {"start_marker": {"labels": labels_2}},
            },
        )

        lss = sl.get_line_segments()
        (start_1, _), (start_2, _) = lss[1].get_markers(), lss[3].get_markers()
        assert len(start_1.get_labels()) == 2
        assert len(start_2.get_labels()) == 3
        check_straight_line_alignment(sl)
        check_all_straight_lines_centered(sl)

    def test_get_labels(self):
        labels_1 = [
            Label(text="First first layer", offset=(0, 20)),
            Label(text="First second layer", offset=(0, 10)),
        ]
        labels_2 = [
            Label(text="Second first layer", offset=(0, 5)),
            Label(text="Second second layer", offset=(0, 2)),
            Label(text="Second third layer"),
        ]

        sl = SegmentedLine(
            type=LineOrientation.HORIZONTAL,
            segment_lengths=self.lengths,
            thickness=5,
            options={
                2: {"start_marker": {"labels": labels_1}},
                4: {"start_marker": {"labels": labels_2}},
            },
        )

        assert set([label.text for label in sl.get_labels()]) == set(
            [label.text for label in labels_1 + labels_2]
        )


class VerticalSegmentedLineTestCase(TestCase):
    def setUp(self) -> None:
        self.lengths = [1, 2, 3.4, 5.6]
        self.sl = SegmentedLine(
            type=LineOrientation.VERTICAL, segment_lengths=self.lengths
        )

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
        plss = self.sl.get_line_segments(positioned=True)
        assert len(plss) == 4

    def test_default_marker_values(self):
        lss = self.sl.get_line_segments()
        for ls in lss:
            start, end = ls.get_markers()
            assert isinstance(start, Marker)
            assert start.get_length() == 6
            assert start.get_color() == "black"
            assert start.show is True

            if ls != lss[-1]:
                assert end is None
            else:
                assert isinstance(end, Marker)
                assert end.get_length() == 6
                assert end.get_color() == "black"

    def test_setting_default_marker_length(self):
        sl = SegmentedLine(
            type=LineOrientation.VERTICAL,
            segment_lengths=self.lengths,
            marker_length=100,
        )
        for ls in sl.get_line_segments():
            start, end = ls.get_markers()
            assert start.get_length() == 100
            if end:
                assert end.get_length() == 100

    def test_aligned_segmented_lines(self):
        lengths = [1, 2, 3.4, 5.6]
        sl = SegmentedLine(type=LineOrientation.VERTICAL, segment_lengths=lengths)

        check_all_straight_lines_centered(sl)
        check_straight_line_alignment(sl)

    def test_different_marker_lengths(self):
        sl = SegmentedLine(
            type=LineOrientation.VERTICAL,
            segment_lengths=self.lengths,
            marker_length=100,
            options={2: {"start_marker": {"length": 10}}},
        )

        for index, ls in enumerate(sl.get_line_segments()):
            if index == 1:
                assert ls.get_markers()[0].get_length() == 10
            else:
                assert ls.get_markers()[0].get_length() == 100
        check_all_straight_lines_centered(sl)
        check_straight_line_alignment(sl)

    def test_add_labels(self):
        labels_1 = [
            Label(text="First first layer", offset=(0, 20)),
            Label(text="First second layer", offset=(0, 10)),
        ]
        labels_2 = [
            Label(text="Second first layer", offset=(0, 5)),
            Label(text="Second second layer", offset=(0, 2)),
            Label(text="Second third layer"),
        ]

        sl = SegmentedLine(
            type=LineOrientation.VERTICAL,
            segment_lengths=self.lengths,
            thickness=5,
            options={
                2: {"start_marker": {"labels": labels_1}},
                4: {"start_marker": {"labels": labels_2}},
            },
        )

        lss = sl.get_line_segments()
        (start_1, _), (start_2, _) = lss[1].get_markers(), lss[3].get_markers()
        assert len(start_1.get_labels()) == 2
        assert len(start_2.get_labels()) == 3
        check_straight_line_alignment(sl)
        check_all_straight_lines_centered(sl)
