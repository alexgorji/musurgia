from pathlib import Path

import pytest

from musurgia.graphics.drawobject import Position
from musurgia.graphics.models import LineOrientation
from musurgia.graphics.page import Page
from musurgia.graphics.ruler import Ruler, RulerUnit
from musurgia.tests.helpers.svg import SVGTestCase

this_path = Path(__file__)


class HorizontalRulerRegressionTests(SVGTestCase):
    def test_horizontal_ruler_unit(self):
        page = Page()
        page.add_grid()
        ru = RulerUnit(
            type=LineOrientation.HORIZONTAL,
            length=20,
            division=5,
            large_markers_length=5,
            small_markers_length=2.5,
            color="blue",
            thickness=1,
        )
        ru.box.show = True

        y = 10
        for p, o in ru.get_draw_objects(positioned=True):
            position = Position(10, y) + p
            page.add_draw_object(position, o)
            y += 10

        page.add_draw_object(Position(10, 60), ru)
        self.compare_page(page, "unit", this_path, height=297 * 2, width=210 * 2)

    @pytest.mark.nonci
    def test_horizontal_ruler(self):
        page = Page()
        page.add_grid()
        page.layout.orientation = "landscape"
        hr = Ruler(
            type=LineOrientation.HORIZONTAL,
            length=60,
            color="blue",
            thickness=1,
            unit_length=20,
            unit_division=5,
        )
        page.add_draw_object(Position(10, 10), hr)

        self.compare_page(page, "", this_path, height=210 * 2, width=297 * 2)
