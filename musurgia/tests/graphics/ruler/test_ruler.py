from dataclasses import asdict
from decimal import Decimal
from pathlib import Path

import pytest


from musurgia.graphics.defaults import DEFAULT_THICKNESS
from musurgia.graphics.geometry import LineOrientation, Position
from musurgia.graphics.ruler import (
    Ruler,
    RulerOptions,
    UnitMarkerOptions,
    _get_division_length,
)
from musurgia.graphics.segmented_line import SegmentedLine
from musurgia.graphics.svg.paginator import SVGPage
from musurgia.tests.helpers.svg import SVGTestCase

this_path = Path(__file__)
# pytestmark = pytest.mark.only


# helper functions


def test_get_division_length():
    ruler_options = RulerOptions()
    assert _get_division_length(ruler_options) == 1
    ruler_options = RulerOptions(unit_division=2)
    assert _get_division_length(ruler_options) == 5
    ruler_options = RulerOptions(unit_division=5, unit_length=20)
    assert _get_division_length(ruler_options) == 4


def test_partial_ruler_options():
    ruler_options = RulerOptions(color="red", unit_marker=UnitMarkerOptions(length=10))
    ruler_options.unit_marker.length = 1

    assert asdict(ruler_options) == {
        "unit_marker": {"length": 1},
        "unit_division_marker": {"length": Decimal("3.0")},
        "unit_length": 10,
        "unit_division": 10,
        "labels_interval": 1,
        "label": {
            "offset": (1, 3),
            "color": "black",
            "font_family": "DejaVu Sans",
            "font_size": 10,
        },
        "thickness": DEFAULT_THICKNESS,
        "color": "red",
    }


# ruler


def test_ruler_units():
    hr = Ruler(type=LineOrientation.HORIZONTAL, length=60)
    units = hr.get_units()
    assert len(units) == 6
    assert isinstance(units[0], SegmentedLine)
    assert hr.length == 60
    assert units[0].get_length() == 10
    assert units[0].get_line_segments()[0].length == 1


def test_ruler_as_segmented_line():
    hr = Ruler(type=LineOrientation.HORIZONTAL, length=60)
    assert isinstance(hr.as_segmented_line(), SegmentedLine)
    assert hr.as_segmented_line().get_length() == 60
    hr.build()
    assert hr.get_draw_objects() == [hr.as_segmented_line()]


@pytest.mark.nonci
class RulerDraw(SVGTestCase):
    def test_horizontal_ruler(self):
        page = SVGPage()
        page.add_grid(thickness=Decimal("0.05"))
        hr = Ruler(
            type=LineOrientation.HORIZONTAL,
            length=60,
            options=RulerOptions(unit_length=20),
        )
        hr.options.color = "red"
        hr.options.label.color = "green"
        hr.build()
        page.add_background("white")
        page.add_grid()
        page.add_draw_object(Position(10, 10), hr)

        self.compare_page(page, "horizontal", this_path, height=210 * 2, width=297 * 2)

    def test_vertical_ruler(self):
        page = SVGPage()
        page.add_grid(thickness=Decimal("0.05"))
        vr = Ruler(
            type=LineOrientation.VERTICAL,
            length=60,
            options=RulerOptions(unit_length=20),
        )
        vr.options.color = "red"
        vr.options.label.color = "green"
        vr.build()
        page.add_background("white")
        page.add_grid()
        page.add_draw_object(Position(10, 10), vr)

        self.compare_page(page, "vertical", this_path, height=210 * 2, width=297 * 2)
