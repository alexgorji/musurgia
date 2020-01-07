from unittest import TestCase

from musurgia.fractaltree.fractaltree import FractalTree


class Test(TestCase):
    def setUp(self) -> None:
        self.ft = FractalTree(tree_permutation_order=[3, 1, 2], proportions=[1, 2, 3])

    def test_1(self):
        self.ft.add_layer()
        result = [(2, 1), (2, 2), (2, 3)]
        self.assertEqual([child.multi for child in self.ft.get_children()], result)
