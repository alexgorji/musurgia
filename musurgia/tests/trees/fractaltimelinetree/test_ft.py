from unittest import TestCase
import warnings


from musurgia.trees.fractaltimelinetree import FractalTimelineTree
from musurgia.musurgia_exceptions import (
    FractalTimelineTreePermutationIndexError,
    FractalTimelineTreeSetMainPermutationOrderFirstError,
    FractalTimelineTreeHasChildrenError,
    FractalTimelineTreeMergeWrongValuesError,
    FractalTimelineTreeHasNoChildrenError,
)
from musurgia.tests.utils_for_tests import create_test_fractal_timline_tree
from musurgia.trees.timelinetree import TimelineDuration


class TestFt(TestCase):
    def setUp(self) -> None:
        self.ft = create_test_fractal_timline_tree()

    def test_get_fractal_order(self):
        expected = """└── 0
    ├── 3
    │   ├── 2
    │   ├── 4
    │   │   ├── 2
    │   │   ├── 4
    │   │   ├── 1
    │   │   └── 3
    │   ├── 1
    │   └── 3
    │       ├── 3
    │       ├── 1
    │       ├── 4
    │       └── 2
    ├── 1
    ├── 4
    │   ├── 1
    │   ├── 2
    │   ├── 3
    │   │   ├── 2
    │   │   ├── 4
    │   │   ├── 1
    │   │   └── 3
    │   └── 4
    │       ├── 1
    │       ├── 2
    │       ├── 3
    │       └── 4
    └── 2
        ├── 4
        │   ├── 2
        │   ├── 4
        │   ├── 1
        │   └── 3
        ├── 3
        │   ├── 3
        │   ├── 1
        │   ├── 4
        │   └── 2
        ├── 2
        └── 1
"""
        self.assertEqual(
            self.ft.get_tree_representation(key=lambda node: node.get_fractal_order()),
            expected,
        )

    def test_add_wrong_child(self):
        ft = FractalTimelineTree(duration=TimelineDuration(10), proportions=(1, 2, 3))
        with self.assertRaises(TypeError):
            ft.add_child("something")

    def test_non_root_main_permutation_order(self):
        ft = FractalTimelineTree(duration=TimelineDuration(10), proportions=(1, 2, 3))
        assert ft.main_permutation_order is None
        assert self.ft.main_permutation_order == (3, 1, 4, 2)
        for node in self.ft.traverse():
            assert node.main_permutation_order == self.ft.main_permutation_order

    def test_calculate_permutation_index_error(self):
        ft = FractalTimelineTree(duration=TimelineDuration(10), proportions=(1, 2, 3))
        with self.assertRaises(FractalTimelineTreePermutationIndexError):
            ft.calculate_permutation_index()

        child = ft.add_child(
            FractalTimelineTree(duration=TimelineDuration(5), proportions=(1, 2, 3))
        )
        with self.assertRaises(FractalTimelineTreeSetMainPermutationOrderFirstError):
            child.calculate_permutation_index()
        with self.assertRaises(FractalTimelineTreeHasChildrenError):
            ft.main_permutation_order = (3, 1, 2)

    def test_generate_children_wrong_size(self):
        ft = FractalTimelineTree(
            duration=TimelineDuration(10),
            proportions=(1, 2, 3),
            main_permutation_order=(3, 1, 2),
            permutation_index=(1, 1),
        )
        with self.assertRaises(ValueError):
            ft.generate_children(4)
        with self.assertRaises(ValueError):
            ft.generate_children(-1)
        with self.assertRaises(TypeError):
            ft.generate_children("string")

    def test_get_children_fractal_orders_error(self):
        ft = FractalTimelineTree(duration=TimelineDuration(10), proportions=(1, 2, 3))
        with self.assertRaises(FractalTimelineTreeSetMainPermutationOrderFirstError):
            ft.get_children_fractal_orders()

    def test_merge_reduce_error(self):
        ft = FractalTimelineTree(
            duration=TimelineDuration(10),
            proportions=(1, 2, 3),
            main_permutation_order=(3, 1, 2),
            permutation_index=(1, 1),
        )
        with self.assertRaises(FractalTimelineTreeHasNoChildrenError):
            ft.merge_children(1, 3)
        with self.assertRaises(FractalTimelineTreeHasNoChildrenError):
            ft.reduce_children_by_condition(lambda node: node.get_value() == 10)
        ft.generate_children(3)
        with self.assertRaises(FractalTimelineTreeMergeWrongValuesError):
            ft.merge_children(1, 3)
        with self.assertRaises(ValueError):
            ft.reduce_children_by_size(2, mode="merge")
        with self.assertRaises(ValueError):
            ft.reduce_children_by_size(2, mode="merge", merge_index=20)

        with self.assertRaises(ValueError):
            ft.reduce_children_by_size(5)
        with self.assertRaises(ValueError):
            ft.reduce_children_by_size(-1)
        ft.reduce_children_by_size(0)
        assert len(ft.get_children()) == 3
        ft.reduce_children_by_size(2, mode="merge", merge_index=2)
        assert len(ft.get_children()) == 2

    def test_split_iter(self):
        ft = FractalTimelineTree(
            duration=TimelineDuration(10),
            proportions=(1, 2, 3),
            main_permutation_order=(3, 1, 2),
            permutation_index=(1, 1),
        )
        ft.split([1, 3, 1])
        assert len(ft.get_children()) == 3

    def test_split_error(self):
        with self.assertRaises(FractalTimelineTreeHasChildrenError):
            self.ft.split(1, 2, 3)

    def test_calculate_permutation_index(self):
        ft = FractalTimelineTree(duration=TimelineDuration(10), proportions=(1, 2, 3))
        with self.assertRaises(FractalTimelineTreePermutationIndexError):
            ft.calculate_permutation_index()

    def test_get_children_with_and_without_warning(self):
        ft = FractalTimelineTree(duration=TimelineDuration(10), proportions=(1, 2, 3))
        ft.add_child(
            FractalTimelineTree(duration=TimelineDuration(5), proportions=(1, 2, 3))
        )

        with warnings.catch_warnings(record=True) as w:
            ft.get_children()
            assert len(w) == 1

        with warnings.catch_warnings(record=True) as w:
            ft._get_children()
            assert len(w) == 0
