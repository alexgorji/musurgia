from unittest import TestCase

from musurgia.trees.fractaltimelinetree import FractalTimelineTree
from musurgia.matrix.matrix import PermutationOrderMatrix
from musurgia.musurgia_exceptions import (
    FractalTimelineTreeSetMainPermutationOrderFirstError,
)
from musurgia.trees.timelinetree import TimelineDuration


class TestFractalTreeInit(TestCase):
    def test_init(self):
        with self.assertRaises(TypeError):
            FractalTimelineTree()
        with self.assertRaises(TypeError):
            FractalTimelineTree(duration=TimelineDuration(10))
        with self.assertRaises(TypeError):
            FractalTimelineTree(proportions=(1, 2, 3))
        ft = FractalTimelineTree(duration=TimelineDuration(10), proportions=(1, 2, 3))
        with self.assertRaises(FractalTimelineTreeSetMainPermutationOrderFirstError):
            ft.get_permutation_order_matrix()

    def test_init_creates_matrix(self):
        ft = FractalTimelineTree(
            duration=TimelineDuration(10),
            proportions=(1, 2, 3),
            main_permutation_order=(3, 1, 2),
        )
        assert isinstance(ft.get_permutation_order_matrix(), PermutationOrderMatrix)
        assert ft.get_permutation_order_matrix().matrix_data == [
            [(3, 1, 2), (2, 3, 1), (1, 2, 3)],
            [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
            [(2, 3, 1), (1, 2, 3), (3, 1, 2)],
        ]
        ft.main_permutation_order = (3, 1, 2)
        assert isinstance(ft.get_permutation_order_matrix(), PermutationOrderMatrix)
        assert ft.get_permutation_order_matrix().matrix_data == [
            [(3, 1, 2), (2, 3, 1), (1, 2, 3)],
            [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
            [(2, 3, 1), (1, 2, 3), (3, 1, 2)],
        ]
        ft.add_child(
            FractalTimelineTree(duration=TimelineDuration(10), proportions=(1, 2, 3))
        )
