from pprint import pprint
from unittest import TestCase

from quicktions import Fraction

from musurgia.fractal.fractaltree import FractalTree
from musurgia.utils import flatten


class Test(TestCase):
    def setUp(self) -> None:
        self.ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))

    def test_change_root_value_without_children(self):
        self.ft.change_value(15)
        self.assertEqual(15, self.ft.get_value())

    def test_change_root_value_with_children(self):
        self.ft.add_layer()
        self.ft.change_value(15)
        self.assertEqual(15, self.ft.get_value())
        self.assertEqual(15, sum([child.get_value() for child in self.ft.get_children()]))
        self.assertEqual([Fraction(15, 2), Fraction(5, 2), Fraction(5, 1)],
                         [child.get_value() for child in self.ft.get_children()])

    def test_change_leaf_value(self):
        self.ft.add_layer()
        self.ft.get_children()[0].change_value(10)
        self.assertEqual(15, self.ft.get_value())
        self.assertEqual(15, sum([child.get_value() for child in self.ft.get_layer(1)]))
        self.assertEqual([Fraction(10, 1), Fraction(5, 3), Fraction(10, 3)],
                         [child.get_value() for child in self.ft.get_children()])

    def test_two_layers_change_child_value(self):
        self.ft.add_layer()
        self.ft.add_layer()
        # print(self.ft.get_layer(1, key=lambda node: node.get_value()))
        # [Fraction(5, 1), Fraction(5, 3), Fraction(10, 3)]
        # print(self.ft.get_layer(2, key=lambda node: node.get_value()))
        # [[Fraction(5, 2), Fraction(5, 6), Fraction(5, 3)], [Fraction(5, 9), Fraction(5, 6), Fraction(5, 18)], [Fraction(5, 9), Fraction(10, 9), Fraction(5, 3)]]
        self.ft.get_children()[0].change_value(10)

        self.assertEqual(15, self.ft.get_value())
        self.assertEqual(15, sum(flatten(self.ft.get_layer(1, key=lambda node: node.get_value()))))
        self.assertEqual(15, sum(flatten(self.ft.get_layer(1, key=lambda node: node.get_value()))))
        self.assertEqual([Fraction(10, 1), Fraction(5, 3), Fraction(10, 3)],
                         self.ft.get_layer(1, key=lambda node: node.get_value()))
        self.assertEqual([[Fraction(5, 1), Fraction(5, 3), Fraction(10, 3)],
                          [Fraction(5, 9), Fraction(5, 6), Fraction(5, 18)],
                          [Fraction(5, 9), Fraction(10, 9), Fraction(5, 3)]],
                         self.ft.get_layer(2, key=lambda node: node.get_value()))

    def test_with_remove(self):
        self.ft.add_layer()
        self.ft.add_layer()
        self.ft.add_layer()
        # print(self.ft.get_layer(1, key=lambda leaf: round(float(leaf.get_value()), 2)))
        #  [5.0, 1.67, 3.33]
        # print(self.ft.get_layer(2, key=lambda leaf: round(float(leaf.get_value()), 2)))
        """
        [[2.5, 0.83, 1.67], 
         [0.56, 0.83, 0.28], 
         [0.56, 1.11, 1.67]]
        """
        # pprint(self.ft.get_layer(3, key=lambda leaf: round(float(leaf.get_value()), 2)))
        """
        [[[1.25, 0.42, 0.83], [0.28, 0.42, 0.14], [0.28, 0.56, 0.83]],
         [[0.28, 0.09, 0.19], [0.28, 0.42, 0.14], [0.05, 0.09, 0.14]],
         [[0.28, 0.09, 0.19], [0.37, 0.56, 0.19], [0.28, 0.56, 0.83]]]
        """
        first_child = self.ft.get_children()[0]
        first_child.remove(first_child.get_children()[2])
        first_child.get_children()[1].change_value(2.5)

        self.assertEqual(10, self.ft.get_value())
        self.assertEqual([5.0, 1.67, 3.33], self.ft.get_layer(1, key=lambda leaf: round(float(leaf.get_value()), 2)))
        self.assertEqual([[2.5, 2.5], [0.56, 0.83, 0.28], [0.56, 1.11, 1.67]],
                         self.ft.get_layer(2, key=lambda leaf: round(float(leaf.get_value()), 2)))
        self.assertEqual([[[1.25, 0.42, 0.83], [0.83, 1.25, 0.42]],
                          [[0.28, 0.09, 0.19], [0.28, 0.42, 0.14], [0.05, 0.09, 0.14]],
                          [[0.28, 0.09, 0.19], [0.37, 0.56, 0.19], [0.28, 0.56, 0.83]]],
                         self.ft.get_layer(3, key=lambda leaf: round(float(leaf.get_value()), 2)))
