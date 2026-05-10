from dataclasses import asdict
from decimal import Decimal
from pathlib import Path


from musurgia.graphics.defaults import DEFAULT_THICKNESS
from musurgia.graphics.geometry import LineOrientation, Position
from musurgia.graphics.ruler import (
    Ruler,
    RulerOptions,
    UnitMarkerOptions,
    _get_division_length,
    _get_number_of_divisions,
    _get_number_of_units,
    _ruler_segment_lengths,
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


def test_get_number_of_units():
    ruler_options = RulerOptions()
    assert _get_number_of_units(ruler_options, 40) == 4
    assert _get_number_of_units(ruler_options, 44) == Decimal("4.4")
    assert _get_number_of_units(ruler_options, Decimal("44.6")) == Decimal("4.46")


def test_get_number_of_divisions():
    ruler_options = RulerOptions()
    assert _get_number_of_divisions(ruler_options, Decimal("44.6")) == 44
    ruler_options = RulerOptions(unit_length=40, unit_division=5)
    assert _get_number_of_divisions(ruler_options, 100) == 12


def test_ruler_segment_lengths():
    ruler_options = RulerOptions()
    segment_lengths = _ruler_segment_lengths(ruler_options, 20)
    assert len(segment_lengths) == 20
    assert segment_lengths[0] == 1
    assert sum(segment_lengths) == 20

    segment_lengths = _ruler_segment_lengths(ruler_options, Decimal("23.6"))
    assert len(segment_lengths) == 23
    assert sum(segment_lengths) == 23

    ruler_options = RulerOptions(unit_length=40, unit_division=5)
    segment_lengths = _ruler_segment_lengths(ruler_options, 100)
    assert len(segment_lengths) == 12
    assert sum(segment_lengths) == 96


# def test_create_segmented_line_options():
#     ruler_options = RulerOptions()
#     sl_options = _create_segmented_line_options(ruler_options, 20)
#     assert len(sl_options) == 20
#     for key, opt in sl_options.items():
#         start_marker_options = opt.get("start_marker")
#         assert start_marker_options
#         if (key - 1) % ruler_options.unit_division == 0:
#             assert start_marker_options["length"] == ruler_options.unit_marker.length
#             assert (
#                 start_marker_options["thickness"] == ruler_options.unit_marker.thickness
#             )


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


class RulerDraw(SVGTestCase):
    def test_horizontal_ruler(self):
        page = SVGPage()
        page.add_grid(thickness=Decimal("0.05"))
        hr = Ruler(
            type=LineOrientation.HORIZONTAL,
            length=60,
            options=RulerOptions(thickness=2, unit_length=20),
        )
        hr.options.color = "red"
        hr.options.label.color = "green"
        hr.build()
        page.add_background("white")
        page.add_grid()
        page.add_draw_object(Position(10, 10), hr)

        self.compare_page(page, "", this_path, height=210 * 2, width=297 * 2)


#     def test_vertical_ruler(self):
#         page = SVGPage(layout=PageLayout(orientation="landscape"))
#         page.add_grid(thickness=Decimal("0.05"))
#         vr = Ruler(
#             type=LineOrientation.VERTICAL,
#             length=60,
#             options={
#                 "thickness": 1,
#                 "unit_length": 20,
#                 "unit_division": 5,
#                 "label": {"color": "green"},
#             },
#         )
#         vr.options.color = "red"
#         vr.options.lable.color = "green"

#         page.add_draw_object(Position(10, 10), hr)

#         self.compare_page(page, "vertical", this_path, height=210 * 2, width=297 * 2)
