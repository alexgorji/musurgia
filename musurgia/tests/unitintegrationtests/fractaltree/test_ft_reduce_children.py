from pprint import pprint
from unittest import TestCase

from musurgia.fractal.fractaltree import FractalTree
from musurgia.utils import flatten


class TestFractalTreeReduceChildrenByCondition(TestCase):

    def test_reduce_first_layer(self):
        ft = FractalTree(proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), value=20)
        ft.add_layer()
        ft.add_layer()
        for node in ft.get_layer(1):
            node.reduce_children_by_condition(condition=lambda node: node.get_fractal_order() == 1)
        self.assertEqual([3, 2, 2, 3, 2, 3], [node.get_fractal_order() for node in ft.iterate_leaves()])

    def test_value(self):
        ft = FractalTree(proportions=[1, 2, 3, 4, 5, 6], main_permutation_order=(4, 1, 5, 3, 6, 2), value=20)
        ft.add_layer()
        ft.reduce_children_by_condition(lambda child: child.get_fractal_order() not in [2, 3])
        self.assertEqual([3, 2], [node.get_fractal_order() for node in ft.iterate_leaves()])
        self.assertEqual([12, 8], [node.get_value() for node in ft.get_children()])


class TestFractalTreeReduceChildrenByNumberOfChildren(TestCase):

    def test_reduce_backward(self):
        ft = FractalTree(proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), value=20)
        ft.add_layer()
        ft.add_layer()
        ft.reduce_children_by_size(size=2)
        self.assertEqual([3, 2], ft.get_layer(1, key=lambda node: node.get_fractal_order()))
        self.assertEqual([12, 8], ft.get_layer(1, key=lambda node: node.get_value()))
        self.assertEqual([[3, 1, 2], [1, 2, 3]], ft.get_layer(2, key=lambda node: node.get_fractal_order()))
        self.assertEqual([[6, 2, 4], [1.33, 2.67, 4]],
                         ft.get_layer(2, key=lambda node: round(float(node.get_value()), 2)))

    def test_reduce_forwards(self):
        ft = FractalTree(proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), value=20)
        ft.add_layer()
        ft.add_layer()
        ft.reduce_children_by_size(size=2, mode='forwards')
        self.assertEqual([1, 2], ft.get_layer(1, key=lambda node: node.get_fractal_order()))
        self.assertEqual([6.67, 13.33], ft.get_layer(1, key=lambda node: round(float(node.get_value()), 2)))
        self.assertEqual([[2, 3, 1], [1, 2, 3]], ft.get_layer(2, key=lambda node: node.get_fractal_order()))
        self.assertEqual([[2.22, 3.33, 1.11], [2.22, 4.44, 6.67]],
                         ft.get_layer(2, key=lambda node: round(float(node.get_value()), 2)))

    def test_reduce_sieve(self):
        ft = FractalTree(proportions=(1, 2, 3, 4, 5, 6, 7), main_permutation_order=(5, 3, 1, 6, 2, 7, 4), value=20)
        ft.add_layer()
        ft.add_layer()
        ft.reduce_children_by_size(size=3, mode='sieve')
        self.assertEqual([1, 7, 4], ft.get_layer(1, key=lambda node: node.get_fractal_order()))
        self.assertEqual([1.67, 11.67, 6.67], ft.get_layer(1, key=lambda node: round(float(node.get_value()), 2)))
        self.assertEqual([[3, 5, 2, 4, 1, 6, 7], [2, 1, 5, 4, 3, 6, 7], [3, 5, 2, 6, 1, 7, 4]],
                         ft.get_layer(2, key=lambda node: node.get_fractal_order()))
        self.assertEqual([[0.18, 0.3, 0.12, 0.24, 0.06, 0.36, 0.42],
                          [0.83, 0.42, 2.08, 1.67, 1.25, 2.5, 2.92],
                          [0.71, 1.19, 0.48, 1.43, 0.24, 1.67, 0.95]],
                         ft.get_layer(2, key=lambda node: round(float(node.get_value()), 2)))

    def test_merge(self):
        ft_1 = FractalTree(proportions=(1, 2, 3, 4, 5, 6, 7), main_permutation_order=(5, 3, 1, 6, 2, 7, 4), value=20)
        ft_2 = FractalTree(proportions=(1, 2, 3, 4, 5, 6, 7), main_permutation_order=(5, 3, 1, 6, 2, 7, 4), value=20)
        ft_3 = FractalTree(proportions=(1, 2, 3, 4, 5, 6, 7), main_permutation_order=(5, 3, 1, 6, 2, 7, 4), value=20)
        for i in range(2):
            ft_1.add_layer()
            ft_2.add_layer()
            ft_3.add_layer()
        self.assertEqual([4, 1, 1, 1], ft_1._get_merge_lengths(size=4, merge_index=0))
        self.assertEqual([1, 1, 4, 1], ft_1._get_merge_lengths(size=4, merge_index=2))
        self.assertEqual([2, 1, 4], ft_3._get_merge_lengths(size=3, merge_index=3))
        # print(ft_1.get_layer(1, key=lambda node: round(float(node.get_value()), 2)))
        #  [3.57, 2.14, 0.71, 4.29, 1.43, 5.0, 2.86]
        # pprint(ft_1.get_layer(2, key=lambda node: node.get_fractal_order()))
        """
        [[5, 3, 1, 6, 2, 7, 4],
         [2, 1, 5, 7, 3, 4, 6],
         [3, 5, 2, 4, 1, 6, 7],
         [1, 2, 3, 6, 5, 7, 4],
         [5, 3, 1, 7, 2, 4, 6],
         [2, 1, 5, 4, 3, 6, 7],
         [3, 5, 2, 6, 1, 7, 4]]
        """
        ft_1.reduce_children_by_size(size=4, mode='merge', merge_index=0)
        ft_2.reduce_children_by_size(size=4, mode='merge', merge_index=2)
        ft_3.reduce_children_by_size(size=3, mode='merge', merge_index=3)
        self.assertEqual([5, 2, 7, 4], ft_1.get_layer(1, key=lambda node: node.get_fractal_order()))
        self.assertEqual([5, 3, 1, 4], ft_2.get_layer(1, key=lambda node: node.get_fractal_order()))
        self.assertEqual([5, 1, 6], ft_3.get_layer(1, key=lambda node: node.get_fractal_order()))
        self.assertEqual([10.71, 1.43, 5.0, 2.86],
                         ft_1.get_layer(1, key=lambda node: round(float(node.get_value()), 2)))
        self.assertEqual([[5, 3, 1, 6, 2, 7, 4],
                          [5, 3, 1, 7, 2, 4, 6],
                          [2, 1, 5, 4, 3, 6, 7],
                          [3, 5, 2, 6, 1, 7, 4]],
                         ft_1.get_layer(2, key=lambda node: node.get_fractal_order()))
        self.assertEqual([[1.91, 1.15, 0.38, 2.3, 0.77, 2.68, 1.53],
                          [0.26, 0.15, 0.05, 0.36, 0.1, 0.2, 0.31],
                          [0.36, 0.18, 0.89, 0.71, 0.54, 1.07, 1.25],
                          [0.31, 0.51, 0.2, 0.61, 0.1, 0.71, 0.41]],
                         ft_1.get_layer(2, key=lambda node: round(float(node.get_value()), 2)))
        for ft in [ft_1, ft_2, ft_3]:
            assert ft.get_value() == sum(flatten(ft.get_layer(1, key=lambda node: node.get_value()))) == sum(
                flatten(ft.get_layer(2, key=lambda node: node.get_value())))
