from unittest import TestCase

from musurgia.graphics.drawobject import Position
from musurgia.graphics.models import LineOrientation
from musurgia.graphics.util import toggle_line_orientation, toggle_position


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
