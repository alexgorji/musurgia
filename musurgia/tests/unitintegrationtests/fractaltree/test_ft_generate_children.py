from unittest import TestCase

from musurgia.fractal.fractaltree import FractalTree


class TestGenerateChildrenReduce(TestCase):
    def setUp(self) -> None:
        self.ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))

    def test_number_of_children_0(self):
        self.ft.generate_children(number_of_children=0)
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [None]

    def test_number_of_children_1(self):
        self.ft.generate_children(number_of_children=1)
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [3]

    def test_number_of_children_2(self):
        self.ft.generate_children(number_of_children=2)
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [3, 2]

    def test_number_of_children_3(self):
        self.ft.generate_children(number_of_children=3)
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [3, 1, 2]

    def test_with_children_error(self):
        self.ft.generate_children(number_of_children=3)
        with self.assertRaises(ValueError):
            self.ft.generate_children(number_of_children=1)

    def test_tuple_number_of_children_1(self):
        self.ft.generate_children(number_of_children=(1, 1, 1))
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [[3], [3], [3]]

    def test_tuple_number_of_children_2(self):
        self.ft.generate_children(number_of_children=(2, 2, 2))
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [[3, 2], [2, 3], [2, 3]]

    def test_tuple_number_of_children_3(self):
        self.ft.generate_children(number_of_children=(3, 3, 3))
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [[3, 1, 2], [2, 3, 1], [1, 2, 3]]

    def test_tuple_number_of_children_mixed_1_to_3(self):
        self.ft.generate_children(number_of_children=(1, 2, 3))
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [[3, 1, 2], [3], [2, 3]]

    def test_tuple_number_of_children_mixed_0_to_2(self):
        self.ft.generate_children(number_of_children=(0, 1, 2))
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [[3, 2], 1, [3]]

    def test_tuple_number_of_children_mixed_tuples(self):
        self.ft.generate_children(number_of_children=(1, (1, 2, 3), 3))
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [[3, 1, 2], [3],
                                                                                 [[3], [2, 3], [1, 2, 3]]]

    def test_tuple_number_of_children_mixed_tuples_2(self):
        self.ft.generate_children(number_of_children=((1, 3), 2, (1, (1, 3), 3)))
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [[[1, 2, 3], [3], [[3], [3, 1, 2]]],
                                                                                 [[3], [1, 2, 3]], [2, 3]]

    def test_tuple_number_of_children_mixed_tuples_2_forwards(self):
        self.ft.generate_children(number_of_children=((1, 3), 2, (1, (1, 3), 3)), reduce_mode='forwards')
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [[[1], [2, 3, 1]], [2, 1], [[1], [[1], [3, 1, 2]], [1, 2, 3]]]

    def test_tuple_number_of_children_mixed_tuples_2_sieve(self):
        self.ft.generate_children(number_of_children=((1, 3), 2, (1, (1, 3), 3)), reduce_mode='sieve')
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [[[1], [3, 1, 2]], [3, 1],
                                                                                 [[1], [[1], [3, 1, 2]], [1, 2, 3]]]

    def test_tuple_number_of_children_mixed_tuples_2_merge(self):
        self.ft.generate_children(number_of_children=((1, 3), 2, (1, (1, 3), 3)), reduce_mode='merge', merge_index=1)
        assert self.ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()) == [[[1], [3, 1, 2]], [2, 3],
                                                                                 [[3], [[2], [1, 2, 3]], [1, 2, 3]]]
