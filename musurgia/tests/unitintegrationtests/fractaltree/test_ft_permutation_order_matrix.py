from unittest import TestCase

from musurgia.fractal.fractaltree import FractalTree
from musurgia.musurgia_exceptions import FractalTreeHasChildrenError, \
    FractalTreeNonRootCannotSetMainPermutationOrderError
from musurgia.permutation.permutation import permute


class TestFractalTreePOM(TestCase):
    def setUp(self):
        self.ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))

    def test_set_get_pom(self):
        self.ft.main_permutation_order = (3, 1, 4, 2)
        assert self.ft.get_permutation_order_matrix().matrix_data == [
            [(3, 1, 4, 2), (4, 3, 2, 1), (2, 4, 1, 3), (1, 2, 3, 4)],
            [(2, 4, 1, 3), (3, 1, 4, 2), (1, 2, 3, 4), (4, 3, 2, 1)],
            [(1, 2, 3, 4), (2, 4, 1, 3), (4, 3, 2, 1), (3, 1, 4, 2)],
            [(4, 3, 2, 1), (1, 2, 3, 4), (3, 1, 4, 2), (2, 4, 1, 3)]]
        self.ft.add_child(FractalTree(value=10, proportions=(1, 2, 3)))
        with self.assertRaises(FractalTreeHasChildrenError):
            self.ft.main_permutation_order = 'something'

    def test_get_children_permutation_order_matrix(self):
        assert [matrix.matrix_data for matrix in self.ft._get_children_permutation_order_matrices()] == [
            [[(2, 3, 1), (1, 2, 3), (3, 1, 2)],
             [(3, 1, 2), (2, 3, 1), (1, 2, 3)],
             [(1, 2, 3), (3, 1, 2), (2, 3, 1)]],
            [[(1, 2, 3), (3, 1, 2), (2, 3, 1)],
             [(2, 3, 1), (1, 2, 3), (3, 1, 2)],
             [(3, 1, 2), (2, 3, 1), (1, 2, 3)]],
            [[(3, 1, 2), (2, 3, 1), (1, 2, 3)],
             [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
             [(2, 3, 1), (1, 2, 3), (3, 1, 2)]]
        ]

    def test_add_child_with_main_permutation_order_exception(self):
        with self.assertRaises(FractalTreeNonRootCannotSetMainPermutationOrderError):
            self.ft.add_child(FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2)))
        self.ft.add_child(FractalTree(value=10, proportions=(1, 2, 3)))
        with self.assertRaises(FractalTreeNonRootCannotSetMainPermutationOrderError):
            self.ft.get_children()[0].main_permutation_order = 'something'

    def test_add_layer_and_permutation_order_matrices_and_permutation_order(self):
        """
        [[(3, 1, 2), (2, 3, 1), (1, 2, 3)],
         [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
         [(2, 3, 1), (1, 2, 3), (3, 1, 2)]]

        [[(2, 3, 1), (1, 2, 3), (3, 1, 2)],
         [(3, 1, 2), (2, 3, 1), (1, 2, 3)],
         [(1, 2, 3), (3, 1, 2), (2, 3, 1)]],

        [[(1, 2, 3), (3, 1, 2), (2, 3, 1)],
         [(2, 3, 1), (1, 2, 3), (3, 1, 2)],
         [(3, 1, 2), (2, 3, 1), (1, 2, 3)]],

        [[(3, 1, 2), (2, 3, 1), (1, 2, 3)],
         [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
         [(2, 3, 1), (1, 2, 3), (3, 1, 2)]]



        [[(3, 1, 2), (2, 3, 1), (1, 2, 3)],
         [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
         [(2, 3, 1), (1, 2, 3), (3, 1, 2)]],

        [[(2, 3, 1), (1, 2, 3), (3, 1, 2)],
         [(3, 1, 2), (2, 3, 1), (1, 2, 3)],
         [(1, 2, 3), (3, 1, 2), (2, 3, 1)]],

        [[(1, 2, 3), (3, 1, 2), (2, 3, 1)],
         [(2, 3, 1), (1, 2, 3), (3, 1, 2)],
         [(3, 1, 2), (2, 3, 1), (1, 2, 3)]]



        [[(1, 2, 3), (3, 1, 2), (2, 3, 1)],
         [(2, 3, 1), (1, 2, 3), (3, 1, 2)],
         [(3, 1, 2), (2, 3, 1), (1, 2, 3)]],

        [[(3, 1, 2), (2, 3, 1), (1, 2, 3)],
         [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
         [(2, 3, 1), (1, 2, 3), (3, 1, 2)]],

        [[(2, 3, 1), (1, 2, 3), (3, 1, 2)],
         [(3, 1, 2), (2, 3, 1), (1, 2, 3)],
         [(1, 2, 3), (3, 1, 2), (2, 3, 1)]],

        """
        pos = {
            'root': (3, 2, 1),
            '1.1': (2, 3, 1), '1.2': (1, 2, 3), '1.3': (3, 1, 2),

            '2.1.1': (3, 1, 2), '2.1.2': (2, 3, 1), '2.1.3': (1, 2, 3),
            '2.2.1': (1, 2, 3), '2.2.2': (3, 1, 2), '2.2.3': (2, 3, 1),
            '2.3.1': (2, 3, 1), '2.3.2': (1, 2, 3), '2.3.3': (3, 1, 2),

            '3.1.1.1': (1, 2, 3), '3.1.1.2': (3, 1, 2), '3.1.1.3': (2, 3, 1),
            '3.1.2.1': (2, 3, 1), '3.1.2.2': (1, 2, 3), '3.1.2.3': (3, 1, 2),
            '3.1.3.1': (3, 1, 2), '3.1.3.2': (2, 3, 1), '3.1.3.3': (1, 2, 3),

            '3.2.1.1': (2, 3, 1), '3.2.1.2': (1, 2, 3), '3.2.1.3': (3, 1, 2),
            '3.2.2.1': (3, 1, 2), '3.2.2.2': (2, 3, 1), '3.2.2.3': (1, 2, 3),
            '3.2.3.1': (1, 2, 3), '3.2.3.2': (3, 1, 2), '3.2.3.3': (2, 3, 1),

            '3.3.1.1': (3, 1, 2), '3.3.1.2': (2, 3, 1), '3.3.1.3': (1, 2, 3),
            '3.3.2.1': (1, 2, 3), '3.3.2.2': (3, 1, 2), '3.3.2.3': (2, 3, 1),
            '3.3.3.1': (2, 3, 1), '3.3.3.2': (1, 2, 3), '3.3.3.3': (3, 1, 2),

        }
        assert self.ft.get_permutation_order_matrix().matrix_data == [
            [(3, 1, 2), (2, 3, 1), (1, 2, 3)],
            [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
            [(2, 3, 1), (1, 2, 3), (3, 1, 2)]]
        assert self.ft.get_permutation_order() == (3, 1, 2)
        self.ft.add_layer()
        assert [leaf.get_permutation_order() for leaf in self.ft.iterate_leaves()] == [(3, 1, 2), (2, 3, 1), (1, 2, 3)]
        self.ft.add_layer()
        assert [leaf.get_permutation_order() for leaf in self.ft.get_children()[0].iterate_leaves()] == [(2, 3, 1),
                                                                                                         (1, 2, 3),
                                                                                                         (3, 1, 2)]

        assert [leaf.get_permutation_order() for leaf in self.ft.get_children()[1].iterate_leaves()] == [(3, 1, 2),
                                                                                                         (2, 3, 1),
                                                                                                         (1, 2, 3)]

        assert [leaf.get_permutation_order() for leaf in self.ft.get_children()[2].iterate_leaves()] == [(1, 2, 3),
                                                                                                         (3, 1, 2),
                                                                                                         (2, 3, 1)]

        assert False
        assert self.ft.get_children()[0].get_permutation_order_matrix().matrix_data == [
            [(2, 3, 1), (1, 2, 3), (3, 1, 2)],
            [(3, 1, 2), (2, 3, 1), (1, 2, 3)],
            [(1, 2, 3), (3, 1, 2), (2, 3, 1)]]
        assert self.ft.get_children()[1].get_permutation_order_matrix().matrix_data == [
            [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
            [(2, 3, 1), (1, 2, 3), (3, 1, 2)],
            [(3, 1, 2), (2, 3, 1), (1, 2, 3)]]
        assert self.ft.get_children()[2].get_permutation_order_matrix().matrix_data == [
            [(3, 1, 2), (2, 3, 1), (1, 2, 3)],
            [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
            [(2, 3, 1), (1, 2, 3), (3, 1, 2)]]
        self.ft.add_layer()
        assert self.ft.get_children()[0].get_children()[0].get_permutation_order_matrix().matrix_data == [
            [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
            [(2, 3, 1), (1, 2, 3), (3, 1, 2)],
            [(3, 1, 2), (2, 3, 1), (1, 2, 3)]]
        assert self.ft.get_children()[0].get_children()[1].get_permutation_order_matrix().matrix_data == [
            [(3, 1, 2), (2, 3, 1), (1, 2, 3)],
            [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
            [(2, 3, 1), (1, 2, 3), (3, 1, 2)]]
        assert self.ft.get_children()[0].get_children()[2].get_permutation_order_matrix().matrix_data == [
            [(2, 3, 1), (1, 2, 3), (3, 1, 2)],
            [(3, 1, 2), (2, 3, 1), (1, 2, 3)],
            [(1, 2, 3), (3, 1, 2), (2, 3, 1)]]
        assert self.ft.get_children()[1].get_children()[0].get_permutation_order_matrix().matrix_data == [
            [(3, 1, 2), (2, 3, 1), (1, 2, 3)],
            [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
            [(2, 3, 1), (1, 2, 3), (3, 1, 2)]]
