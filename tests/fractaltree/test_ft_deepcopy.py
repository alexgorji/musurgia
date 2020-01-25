from unittest import TestCase

from musurgia.fractaltree.fractaltree import FractalTree


class Test(TestCase):
    def setUp(self) -> None:
        ft = FractalTree(value=10, reading_direction='vertical')
        ft.add_layer()
        ft.add_layer()
        self.ft = ft.get_children()[1]
        self.deep_copied = self.ft.__deepcopy__()

    def test(self, exp=None, act=None):
        if not exp:
            exp = self.ft

        if not act:
            act = self.deep_copied

        self.assertEqual(exp.value, act.value)
        self.assertEqual(exp.proportions, act.proportions)
        self.assertEqual(exp.value, act.value)
        self.assertEqual(exp.proportions, act.proportions)
        self.assertEqual(exp.tree_permutation_order, act.tree_permutation_order)
        self.assertEqual(exp.fractal_order, act.fractal_order)
        self.assertEqual(exp.reading_direction, act.reading_direction)
        self.assertEqual(exp.__name__, act.__name__)
        self.assertNotEqual(exp.up, act.up)

    def test_7(self):
        # print(self.ft.up)
        # print(self.deep_copied.up)
        self.assertNotEqual(self.ft.up, self.deep_copied.up)

    def test_8(self):
        children = self.ft.get_children()
        deep_copied_children = self.deep_copied.get_children()
        self.assertEqual(len(children), len(deep_copied_children))

    def test_9(self):
        children = self.ft.get_children()
        deep_copied_children = self.deep_copied.get_children()
        for child, deep_copied_child in zip(children, deep_copied_children):
            self.test(child, deep_copied_child)
