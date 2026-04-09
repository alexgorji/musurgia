from decimal import Decimal
from pathlib import Path
import pytest

from musurgia.graphics.geometry import Position
from musurgia.graphics.geometry import LineOrientation
from musurgia.graphics.ruler import Ruler
from musurgia.graphics.svg.paginator import SVGPage
from musurgia.tests.helpers.svg import SVGTestCase

this_path = Path(__file__)


class HorizontalRulerRegressionTests(SVGTestCase):

    @pytest.mark.nonci
    def test_horizontal_ruler(self):
        page = SVGPage()
        page.add_grid(thickness=Decimal("0.05"))
        hr = Ruler(
            type=LineOrientation.HORIZONTAL,
            length=60,
            color="blue",
            options={
                "thickness": 1,
                "unit_length": 20,
                "unit_division": 5,
                "label": {"color": "green"},
            },
        )
        page.add_draw_object(Position(10, 10), hr)

        self.compare_page(page, "", this_path, height=210 * 2, width=297 * 2)
