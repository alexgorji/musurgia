from pathlib import Path
from musurgia.graphics.drawobject import Position
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
