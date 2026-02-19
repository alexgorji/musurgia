from pathlib import Path

from musurgia.graphics.drawobject import Position
from musurgia.graphics.page import Page
from musurgia.graphics.segmented_line import HorizontalSegmentedLine
from musurgia.tests.helpers.svg import SVGTestCase

this_path = Path(__file__)


class SegmentedLineRegressionTests(SVGTestCase):
    def test_line_segment(self):
        page = Page()
        hsl = HorizontalSegmentedLine(length=25, color="blue", thickness=1)
        print(hsl.get_draw_objects(recursive=True))
        page.add_draw_object(Position(10, 10), hsl)

        self.compare_page(
            page, "line_segment", this_path, width=210 * 2, height=297 * 2
        )
