from pathlib import Path
from musurgia.graphics.geometry import Position
from musurgia.graphics.line_segment import LineSegment
from musurgia.graphics.geometry import LineOrientation
from musurgia.graphics.svg.paginator import SVGPage
from musurgia.tests.helpers.svg import SVGTestCase

this_path = Path(__file__)


class VerticalLineSegmentRegressionTests(SVGTestCase):
    def test_vertical_line_segment(self):
        page = SVGPage()
        page.add_grid()
        vsl = LineSegment(
            type=LineOrientation.VERTICAL, length=25, color="blue", thickness=1
        )

        page.add_draw_object(Position(10, 10), vsl)

        self.compare_page(page, "", this_path, width=210 * 2, height=297 * 2)
