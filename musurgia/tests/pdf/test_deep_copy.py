import copy
from unittest import TestCase
from musurgia.pdf import HorizontalLineSegment


class TestDeepCopy(TestCase):
    def test_horizontal_line_segment(self):
        hls = HorizontalLineSegment(length=10)
        hls.bottom_margin = 30
        hls.relative_x = 20
        hls.start_mark_line.add_text_label('start', font_size=15, bottom_margin=50)
        hls.end_mark_line.add_text_label('stop', font_size=25, position='below', top_margin=40)

        copied = copy.deepcopy(hls)
        assert copied != hls
        assert copied.length == hls.length
        assert copied.mode == hls.mode
        assert copied.straight_line != hls.straight_line
        assert copied.start_mark_line != hls.start_mark_line
        assert copied.end_mark_line != hls.end_mark_line
        assert copied.get_positions() == hls.get_positions()
        assert copied.get_margins() == hls.get_margins()
        start_mark_text_label = hls.start_mark_line.get_text_labels()[0]
        copied_start_mark_text_label = copied.start_mark_line.get_text_labels()[0]
        end_mark_text_label = hls.end_mark_line.get_text_labels()[0]
        copied_end_mark_text_label = copied.end_mark_line.get_text_labels()[0]

        assert start_mark_text_label != copied_start_mark_text_label
        assert end_mark_text_label != copied_end_mark_text_label
        assert start_mark_text_label.get_positions() == copied_start_mark_text_label.get_positions()
        assert end_mark_text_label.get_positions() == copied_end_mark_text_label.get_positions()
        assert start_mark_text_label.get_margins() == copied_start_mark_text_label.get_margins()
        assert end_mark_text_label.get_margins() == copied_end_mark_text_label.get_margins()

        assert start_mark_text_label.value == copied_start_mark_text_label.value
        assert end_mark_text_label.value == copied_end_mark_text_label.value
