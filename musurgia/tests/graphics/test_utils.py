from unittest import TestCase

from musurgia.graphics.geometry import Position
from musurgia.graphics.geometry import LineOrientation
from musurgia.graphics.util import (
    override_options_mappings,
    toggle_line_orientation,
    toggle_position,
)


class Toggles(TestCase):
    def test_toggle_line_orientations(self):
        o = LineOrientation.HORIZONTAL
        toggled = toggle_line_orientation(o)
        assert toggled == LineOrientation.VERTICAL
        assert toggle_line_orientation(toggled) == o

    def test_toggle_postions(self):
        p = Position(100, 200)
        toggled = toggle_position(p)
        assert toggled == Position(200, 100)
        assert toggle_position(toggled) == p


class OverrideOptionsMappings(TestCase):
    def test_override_simple(self):
        options = {"start_marker": {"length": 10, "color": "blue"}}
        override = {
            "start_marker": {"length": 20},
            "end_marker": {"length": 30, "color": "red"},
        }
        assert override_options_mappings(options, override) == {
            "start_marker": {"length": 20, "color": "blue"},
            "end_marker": {"length": 30, "color": "red"},
        }
