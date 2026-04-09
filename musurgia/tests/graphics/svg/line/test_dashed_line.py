from pathlib import Path

from musurgia.graphics.drawobject import StraightLineDrawObject
from musurgia.graphics.geometry import LineOrientation, Position
from musurgia.graphics.svg.paginator import SVGPage
from musurgia.tests.helpers.svg import SVGTestCase


this_path = Path(__file__)


class DashedLineTestCase(SVGTestCase):
    def test_dashed_lines(self):
        page = SVGPage()
        hl = StraightLineDrawObject(
            type=LineOrientation.HORIZONTAL,
            length=100,
            thickness=1,
            color="blue",
            stroke_dasharray=[5, 5],
        )
        page.add_draw_object(Position(10, 10), hl)

        self.compare_page(page, "", this_path, width=297 * 2, height=210 * 2)
