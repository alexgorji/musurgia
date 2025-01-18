from unittest import TestCase

from musurgia.trees.fractaltimelinetree import FractalTimelineTree
from musurgia.trees.timelinetree import TimelineDuration


class TestFtSplit(TestCase):
    def setUp(self):
        self.ft = FractalTimelineTree(
            duration=TimelineDuration(10),
            proportions=(1, 2, 3),
            main_permutation_order=(3, 1, 2),
            permutation_index=(1, 1),
        )
        self.ft.add_layer()
        self.first_child = self.ft.get_children()[0]

    def test_two(self):
        s = self.first_child.split(1, 1)
        actual = [x.get_value() for x in s]
        expected = [self.first_child.get_value() / 2, self.first_child.get_value() / 2]
        self.assertEqual(expected, actual)

    def test_permutation_index(self):
        s = self.first_child.split(1, 1)
        for x in s:
            self.assertEqual(
                x.get_permutation_index(), self.first_child.get_permutation_index()
            )

    def test_three(self):
        s = self.first_child.split(1, 1, 1)
        actual = [x.get_value() for x in s]
        expected = [
            self.first_child.get_value() / 3,
            self.first_child.get_value() / 3,
            self.first_child.get_value() / 3,
        ]
        self.assertEqual(expected, actual)

    def test_split_more_than_size(self):
        s = self.first_child.split(1, 1, 1, 1)
        actual = [x.get_value() for x in s]
        expected = 4 * [self.first_child.get_value() / 4]
        self.assertEqual(expected, actual)

    def test_child_is_not_leaf(self):
        self.first_child.split(1, 1, 1)
        self.assertFalse(self.first_child.is_leaf)

    def test_split_is_leaf(self):
        self.assertTrue(self.first_child.is_leaf)
        s = self.first_child.split(1, 1, 1)
        actual = [x.is_leaf for x in s]
        expected = [True, True, True]
        self.assertEqual(expected, actual)
        self.assertFalse(self.first_child.is_leaf)
        s[0].add_layer()
        self.assertFalse(s[0].is_leaf)
