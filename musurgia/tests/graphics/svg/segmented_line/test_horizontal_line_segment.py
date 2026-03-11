from pathlib import Path
import pytest
from musurgia.graphics.drawobject import Position
from musurgia.graphics.page import Page
from musurgia.graphics.segmented_line import HorizontalLineSegment
from musurgia.tests.helpers.svg import SVGTestCase

this_path = Path(__file__)


@pytest.mark.regression
class HorizontalLineSegmentRegressionTests(SVGTestCase):
    def test_horizontal_line_segment(self):
        page = Page()
        hsl = HorizontalLineSegment(length=25, color="blue", thickness=1)
        page.add_draw_object(Position(10, 10), hsl)

        self.compare_page(page, "", this_path, width=210 * 2, height=297 * 2)
