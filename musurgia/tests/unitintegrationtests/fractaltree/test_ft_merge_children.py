from pprint import pprint

from musurgia.fractal.fractaltree import FractalTree
from musurgia.tests.unitintegrationtests._test_utils import TestCase


class Test(TestCase):
    def test_one_layer(self):
        ft = FractalTree(proportions=(1, 2, 3, 4, 5), main_permutation_order=(3, 5, 1, 2, 4), value=10)
        ft.add_layer()
        ft.merge_children(1, 2, 2)
        self.assertEqual([3, 5, 2], ft.get_leaves(key=lambda leaf: leaf.get_fractal_order()), )
        self.assertEqual([2.0, 4.0, 4.0], ft.get_leaves(key=lambda leaf: round(float(leaf.get_value()), 2)), )

    def test_two_layers(self):
        ft = FractalTree(proportions=(1, 2, 3, 4, 5), main_permutation_order=(3, 5, 1, 2, 4), value=20)
        ft.add_layer()
        ft.add_layer()
        # print(ft.get_layer(1, key=lambda leaf: round(float(leaf.get_value()), 2)))
        #  [4.0, 6.67, 1.33, 2.67, 5.33]
        # pprint(ft.get_layer(2, key=lambda leaf: round(float(leaf.get_value()), 2)))
        """
        [[0.8, 1.33, 0.27, 0.53, 1.07],
         [0.44, 1.78, 1.33, 2.22, 0.89],
         [0.27, 0.18, 0.09, 0.36, 0.44],
         [0.18, 0.89, 0.53, 0.36, 0.71],
         [1.07, 1.42, 0.36, 1.78, 0.71]]
        """
        ft.merge_children(1, 2, 2)
        self.assertEqual([4.0, 8.0, 8.0], ft.get_layer(1, key=lambda leaf: round(float(leaf.get_value()), 2)))
        self.assertEqual([[0.8, 1.33, 0.27, 0.53, 1.07],
                          [0.53, 2.13, 1.6, 2.67, 1.07],
                          [0.53, 2.67, 1.6, 1.07, 2.13]],
                         ft.get_layer(2, key=lambda leaf: round(float(leaf.get_value()), 2)))
