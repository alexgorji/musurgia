import os
from unittest import TestCase

from musurgia.fractaltree.fractaltree import FractalTree

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):

    def test_1(self):
        ft = FractalTree(reading_direction='vertical', value=10)
        ft.add_layer()
        permutation_orders = [child.permutation_order for child in ft.get_children()]
        result = [[2, 1, 3], [3, 2, 1], [1, 3, 2]]
        self.assertEqual(result, permutation_orders)

    def test_2(self):
        ft = FractalTree(tree_permutation_order=(2, 1, 3), reading_direction='vertical', value=10)
        ft.add_layer()
        ft.add_layer()
        permutation_orders = [child.permutation_order for child in ft.get_children()]
        leaves_permuation_order = ft.get_leaves(key=lambda leaf: leaf.permutation_order)
        # print(ft.permutation_order)
        # print(permutation_orders)
        # print(leaves_permuation_order)
        values = [child.value for child in ft.get_children()]
        # print(values)
        # print(sum(values))
        expected = ft.value
        actual = sum(values)
        self.assertEqual(expected, actual)