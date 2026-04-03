from pathlib import Path

import pytest
from musurgia.graphics.drawobject import Position
from musurgia.graphics.line_segment import Label
from musurgia.graphics.page import Page
from musurgia.graphics.models import LineOrientation
from musurgia.graphics.segmented_line import SegmentedLine
from musurgia.tests.helpers.svg import SVGTestCase

this_path = Path(__file__)


class VerticalSegmentedLineRegressionTests(SVGTestCase):
    def test_vertical_segmented_line(self):
        page = Page()
        page.add_grid()
        lengths: list[int | float] = [10, 20, 34, 56]
        sl = SegmentedLine(
            type=LineOrientation.VERTICAL,
            segment_lengths=lengths,
            marker_length=10,
            thickness=3,
            color="blue",
            options={2: {"start_marker": {"length": 20}}},
        )

        page.add_draw_object(Position(10, 10), sl)

        self.compare_page(page, "", this_path, width=297 * 2, height=210 * 2)

    @pytest.mark.nonci
    def test_labeled_vertical_segmented_line(self):
        page = Page()
        page.add_grid()
        lengths: list[int | float] = [10, 20, 34, 56]
        sl = SegmentedLine(
            type=LineOrientation.VERTICAL,
            segment_lengths=lengths,
            marker_length=10,
            thickness=3,
            color="blue",
            options={
                1: {"start_marker": {"labels": [Label(text="1")]}},
                2: {
                    "start_marker": {
                        "length": 20,
                        "labels": [Label(text="2"), Label(text="3", offset=5)],
                    }
                },
                3: {
                    "start_marker": {
                        "labels": [
                            Label(text="4"),
                            Label(text="5", offset=5),
                            Label(text="7", offset=10),
                        ],
                    }
                },
                4: {
                    "start_marker": {
                        "labels": [
                            Label(text="8"),
                            Label(text="9", offset=5),
                            Label(text="10", offset=10),
                            Label(text="11", offset=15),
                        ],
                    },
                    "end_marker": {
                        "labels": [
                            Label(text="12"),
                            Label(text="13", offset=5),
                            Label(text="14", offset=10),
                            Label(text="15", offset=15),
                            Label(text="16", offset=20),
                        ],
                    },
                },
            },
        )
        for label in sl.get_labels():
            label.set_color("green")

        page.add_draw_object(Position(10, 10), sl)

        self.compare_page(page, "labeled", this_path, width=297 * 2, height=210 * 2)
