import os
from unittest import TestCase

from fractions import Fraction

from musurgia.fractal.fractaltree import FractalTree

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def test_two_layers(self):
        ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        ft.add_layer()
        ft.add_layer()
        self.assertEqual(ft.get_number_of_layers(), 2)
        self.assertEqual([[3, 1, 2], [2, 3, 1], [1, 2, 3]], ft.get_leaves(key=lambda node: node.get_fractal_order()))
        self.assertEqual([[2.5, 0.83, 1.67], [0.56, 0.83, 0.28], [0.56, 1.11, 1.67]],
                         ft.get_leaves(key=lambda node: round(float(node.get_value()), 2)))

    def test_with_condition(self):
        ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        ft.add_layer()
        ft.add_layer()
        ft.add_layer(lambda node: node.get_fractal_order() != 1, lambda node: node.get_value() > 0.6)
        self.assertEqual([[[3, 1, 2], 1, [1, 2, 3]], [2, [2, 3, 1], 1], [1, [2, 3, 1], [1, 2, 3]]],
                         ft.get_leaves(key=lambda node: node.get_fractal_order()))

    def test_child_add_layer(self):
        ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        ft.add_layer()
        ft.get_children()[0].add_layer()
        expected = [[2.5, 0.83, 1.67], 1.67, 3.33]
        self.assertEqual(expected, ft.get_leaves(key=lambda leaf: round(float(leaf.get_value()), 2)))
