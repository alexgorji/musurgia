from pathlib import Path

from musurgia.graphics.drawobject import Rectangle, RectangleOptions
from musurgia.graphics.geometry import Position, Size
from musurgia.graphics.svg.paginator import SVGPage
from musurgia.tests.helpers.svg import SVGTestCase

this_path = Path(__file__)


class DashedRectangleTestCase(SVGTestCase):
    def test_dashed_rectangle(self):
        page = SVGPage()
        r = Rectangle(
            size=Size(50, 50),
            options=RectangleOptions(
                thickness=1,
                color="blue",
                stroke_dasharray=[5, 5],
            ),
        )
        page.add_draw_object(Position(40, 40), r)

        self.compare_page(page, "", this_path, width=297 * 2, height=210 * 2)
