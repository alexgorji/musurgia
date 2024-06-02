from unittest import TestCase

from musurgia.pdf.line import StraightLine
from musurgia.tests.utils_for_tests import DummyMaster


class TestStraightLine(TestCase):
    def test_is_horizontal_or_vertical(self):
        line = StraightLine(master=DummyMaster(), value='something', mode='h', length=2)
        assert line.is_horizontal
        assert not line.is_vertical
        line.mode = 'horizontal'
        assert line.is_horizontal
        assert not line.is_vertical
        line.mode = 'vertical'
        assert line.is_vertical
        assert not line.is_horizontal
        line.mode = 'v'
        assert line.is_vertical
        assert not line.is_horizontal

    def test_get_opposite_mode(self):
        assert StraightLine.get_opposite_mode('v') == 'h'
        assert StraightLine.get_opposite_mode('vertical') == 'horizontal'
        assert StraightLine.get_opposite_mode('h') == 'v'
        assert StraightLine.get_opposite_mode('horizontal') == 'vertical'
