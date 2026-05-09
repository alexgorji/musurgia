from pathlib import Path

import pytest
from musurgia.graphics.geometry import Position, Scalar
from musurgia.graphics.line_segment_old import OldLabel
from musurgia.graphics.geometry import LineOrientation
from musurgia.graphics.segmented_line_old import OldSegmentedLine
from musurgia.graphics.svg.paginator import SVGPage
from musurgia.tests.helpers.svg import SVGTestCase

this_path = Path(__file__)


class VerticalSegmentedLineRegressionTests(SVGTestCase):
    def test_vertical_segmented_line(self):
        page = SVGPage()
        page.add_grid()
        lengths: list[Scalar] = [10, 20, 34, 56]
        sl = OldSegmentedLine(
            type=LineOrientation.VERTICAL,
            segment_lengths=lengths,
            marker_length=10,
            thickness=3,
            color="blue",
            options={
                2: {"start_marker": {"length": 20}},
            },
        )

        page.add_draw_object(Position(10, 10), sl)

        self.compare_page(page, "", this_path, width=297 * 2, height=210 * 2)

    @pytest.mark.nonci
    def test_labeled_vertical_segmented_line(self):
        page = SVGPage()
        page.add_grid()
        lengths: list[Scalar] = [10, 20, 34, 56]
        sl = OldSegmentedLine(
            type=LineOrientation.VERTICAL,
            segment_lengths=lengths,
            marker_length=10,
            thickness=3,
            color="blue",
            options={
                1: {"start_marker": {"labels": [OldLabel(text="1")]}},
                2: {
                    "start_marker": {
                        "length": 20,
                        "labels": [
                            OldLabel(text="2"),
                            OldLabel(text="3", offset=(0, 5)),
                        ],
                    }
                },
                3: {
                    "start_marker": {
                        "labels": [
                            OldLabel(text="4"),
                            OldLabel(text="5", offset=(0, 5)),
                            OldLabel(text="7", offset=(0, 10)),
                        ],
                    }
                },
                4: {
                    "start_marker": {
                        "labels": [
                            OldLabel(text="8"),
                            OldLabel(text="9", offset=(0, 5)),
                            OldLabel(text="10", offset=(0, 10)),
                            OldLabel(text="11", offset=(0, 15)),
                        ],
                    },
                    "end_marker": {
                        "labels": [
                            OldLabel(text="12"),
                            OldLabel(text="13", offset=(0, 5)),
                            OldLabel(text="14", offset=(0, 10)),
                            OldLabel(text="15", offset=(0, 15)),
                            OldLabel(text="16", offset=(0, 20)),
                        ],
                    },
                },
            },
        )
        for label in sl.get_labels():
            label.set_color("green")

        page.add_draw_object(Position(10, 10), sl)

        self.compare_page(page, "labeled", this_path, width=297 * 2, height=210 * 2)
