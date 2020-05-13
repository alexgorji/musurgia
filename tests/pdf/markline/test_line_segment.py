from pathlib import Path

from musurgia.pdf.positioned import RelativeXNotSettableError
from musurgia.pdf.segmentedline import LineSegment, MarkLine
from musurgia.unittest import TestCase

path = Path(__file__)


class Test(TestCase):
    def test_relative_set_error(self):
        ls = LineSegment(10, relative_x=11, relative_y=12, bottom_margin=13, left_margin=14, top_margin=15,
                         right_margin=16)
        mk = MarkLine(parent=ls, placement='start')
        with self.assertRaises(RelativeXNotSettableError):
            mk.relative_x = 20


    def test_relative_x_start(self):
        ls = LineSegment(10, relative_x=11, relative_y=12, bottom_margin=13, left_margin=14, top_margin=15,
                         right_margin=16)
        mk = MarkLine(parent=ls, placement='start')
        expected = ls.relative_x
        actual = mk.relative_x
        self.assertEqual(expected, actual)
