from decimal import Decimal
from unittest import TestCase


from musurgia.graphics.geometry import LineOrientation
from musurgia.graphics.ruler_old import (
    Ruler,
    RulerOptions,
    _create_segmented_line_options,
    _get_division_length,
    _get_number_of_divisions,
    _get_number_of_units,
    _ruler_segment_lengths,
)
from musurgia.graphics.segmented_line_old import OldSegmentedLine


class RulerHelperFunctionsTestCase(TestCase):
    def test_get_division_length(self):
        ruler_options = RulerOptions()
        assert _get_division_length(ruler_options) == 1
        ruler_options = RulerOptions(unit_division=2)
        assert _get_division_length(ruler_options) == 5
        ruler_options = RulerOptions(unit_division=5, unit_length=20)
        assert _get_division_length(ruler_options) == 4

    def test_get_number_of_units(self):
        ruler_options = RulerOptions()
        assert _get_number_of_units(ruler_options, 40) == 4
        assert _get_number_of_units(ruler_options, 44) == Decimal("4.4")
        assert _get_number_of_units(ruler_options, Decimal("44.6")) == Decimal("4.46")

    def test_get_number_of_divisions(self):
        ruler_options = RulerOptions()
        assert _get_number_of_divisions(ruler_options, Decimal("44.6")) == 44
        ruler_options = RulerOptions(unit_length=40, unit_division=5)
        assert _get_number_of_divisions(ruler_options, 100) == 12

    def test_ruler_segment_lengths(self):
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

    def test_create_segmented_line_options(self):
        ruler_options = RulerOptions()
        sl_options = _create_segmented_line_options(ruler_options, 20)
        assert len(sl_options) == 20
        print(ruler_options.unit_division)
        for key, opt in sl_options.items():
            start_marker_options = opt.get("start_marker")
            assert start_marker_options
            if (key - 1) % ruler_options.unit_division == 0:
                assert (
                    start_marker_options["length"] == ruler_options.unit_marker.length
                )
                assert (
                    start_marker_options["thickness"]
                    == ruler_options.unit_marker.thickness
                )


class HorizontalRulerTests(TestCase):
    def test_ruler_as_segmented_line(self):
        hr = Ruler(type=LineOrientation.HORIZONTAL, length=60)
        assert isinstance(hr._segmented_line, OldSegmentedLine)
        assert hr._segmented_line.get_length() == 60
        assert len(hr._segmented_line.get_line_segments()) == 60
        for sl in hr._segmented_line.get_line_segments()[:-1]:
            assert sl.get_markers()[1] is None
        assert hr._segmented_line.get_line_segments()[-1].get_markers()[-1] is not None
