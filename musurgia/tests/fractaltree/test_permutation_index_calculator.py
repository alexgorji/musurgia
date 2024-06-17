from unittest import TestCase

from musurgia.fractal.fractaltree import PermutationIndexCalculater


class TestFtUnit(TestCase):

    def test_get_index_error(self):
        pic = PermutationIndexCalculater(size=10)
