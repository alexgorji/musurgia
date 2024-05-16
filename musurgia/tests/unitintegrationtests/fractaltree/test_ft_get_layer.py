from fractions import Fraction
from unittest import TestCase

from musurgia.fractal.fractaltree import FractalTree


class TestGetLayer(TestCase):
    def setUp(self) -> None:
        self.ft = FractalTree(proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), value=10)

    def test_wrong_layer(self):
        with self.assertRaises(Exception):
            self.ft.get_layer(1)

    def test_layer_0(self):
        self.assertEqual(self.ft, self.ft.get_layer(0))

    def test_layer_1(self):
        self.ft.add_layer()
        self.assertEqual(self.ft.get_children(), self.ft.get_layer(1))

    def test_layer_1_of_3(self):
        for i in range(3):
            self.ft.add_layer()
        self.assertEqual(self.ft.get_children(), self.ft.get_layer(1))

    def test_layer_2_of_3(self):
        for i in range(3):
            self.ft.add_layer()
        result = [child.get_children() for child in self.ft.get_children()]

        self.assertEqual(result, self.ft.get_layer(2))

    def test_layer_3_of_3(self):
        for i in range(3):
            self.ft.add_layer()
        result = self.ft.get_leaves()

        self.assertEqual(result, self.ft.get_layer(3))

    def test_layer_wrong_layer_2(self):
        for i in range(3):
            self.ft.add_layer()

        with self.assertRaises(ValueError):
            self.ft.get_layer(4)

    def test_complex_layers(self):
        self.ft.add_layer()
        self.ft.add_layer(lambda n: True if n.get_fractal_order() > 1 else False)
        self.ft.add_layer(lambda n: True if n.get_fractal_order() > 1 else False)
        self.ft.add_layer(lambda n: True if n.get_fractal_order() > 1 else False)
        self.ft.add_layer(lambda n: True if n.get_fractal_order() > 1 else False)
        self.assertEqual([3, 1, 2], self.ft.get_layer(1, key=lambda node: node.get_fractal_order()))
        self.assertEqual([[3, 1, 2], 1, [1, 2, 3]], self.ft.get_layer(2, key=lambda node: node.get_fractal_order()))
        self.assertEqual([[[3, 1, 2], 1, [1, 2, 3]], 1, [1, [2, 3, 1], [1, 2, 3]]],
                         self.ft.get_layer(3, key=lambda node: node.get_fractal_order()))
        self.assertEqual([[[[3, 1, 2], 1, [1, 2, 3]], 1, [1, [2, 3, 1], [1, 2, 3]]],
                          1,
                          [1, [[3, 1, 2], [2, 3, 1], 1], [1, [2, 3, 1], [1, 2, 3]]]],
                         self.ft.get_layer(4, key=lambda node: node.get_fractal_order()))

    def test_layer_values(self):
        self.ft.add_layer()
        self.ft.add_layer()
        self.assertEqual([Fraction(5, 1), Fraction(5, 3), Fraction(10, 3)],
                         self.ft.get_layer(1, key=lambda node: node.get_value()))
        self.assertEqual(
            [[Fraction(5, 2), Fraction(5, 6), Fraction(5, 3)],
             [Fraction(5, 9), Fraction(5, 6), Fraction(5, 18)],
             [Fraction(5, 9), Fraction(10, 9), Fraction(5, 3)]],
            self.ft.get_layer(2, key=lambda node: node.get_value()))
