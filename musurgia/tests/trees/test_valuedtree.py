from unittest import TestCase

from fractions import Fraction
from musurgia.tests.utils_for_tests import DemoValuedTree
from musurgia.utils import flatten

class ValuedTreeChangeValueTestCase(TestCase):
    def setUp(self) -> None:
        self.vt = DemoValuedTree(value=10)

    def _add_layer(self, number_of_layers = 1):
        for value in [5, Fraction(5, 3), Fraction(10, 3)]:
            self.vt.add_child(DemoValuedTree(value=value))
        if number_of_layers == 2:
            list_of_values = [[Fraction(5, 6), Fraction(5, 3), Fraction(5, 2)], [Fraction(5, 6), Fraction(5, 18), Fraction(5, 9)], [Fraction(10, 9), Fraction(5, 3), Fraction(5, 9)]]
            for child, values in zip(self.vt.get_children(), list_of_values):
                for v in values:
                    child.add_child(DemoValuedTree(value=v))


    def test_change_root_value_without_children(self):
        self.vt.change_value(15)
        self.assertEqual(15, self.vt.get_value())

    def test_change_root_value_with_children(self):
        self._add_layer()
        self.vt.change_value(15)
        self.assertEqual(15, self.vt.get_value())
        self.assertEqual(15, sum([child.get_value() for child in self.vt.get_children()]))
        self.assertEqual([Fraction(15, 2), Fraction(5, 2), Fraction(5, 1)],
                         [child.get_value() for child in self.vt.get_children()])

    def test_change_leaf_value(self):
        self._add_layer()
        self.vt.get_children()[0].change_value(10)
        self.assertEqual(15, self.vt.get_value())
        self.assertEqual(15, sum([child.get_value() for child in self.vt.get_layer(1)]))
        self.assertEqual([Fraction(10, 1), Fraction(5, 3), Fraction(10, 3)],
                         [child.get_value() for child in self.vt.get_children()])

    def test_two_layers_change_child_value(self):
        self._add_layer(2)
        self.vt.get_children()[0].change_value(10)
        assert self.vt.get_value() == 15
        assert sum(flatten(self.vt.get_layer(1, key=lambda node: node.get_value()))) == 15
        assert sum(flatten(self.vt.get_layer(2, key=lambda node: node.get_value()))) == 15

    def test_with_remove(self):
        def node_info(node):
            return f"{node.get_position_in_tree()}: {round(float(node.get_value()), 2)}"

        self._add_layer()
        first_child = self.vt.get_children()[0]
        values = [5/6, 5/3, 5/2]
        for v in values:
            first_child.add_child(DemoValuedTree(v))
        list_of_values = [[5/18, 5/12, 5/36], [5/18, 5/9, 5/6], [5/4, 5/12, 5/6]]
        for child, values in zip(first_child.get_children(), list_of_values):
            for v in values:
                child.add_child(DemoValuedTree(v))

        expected = """└── 0: 10.0
    ├── 1: 5.0
    │   ├── 1.1: 0.83
    │   │   ├── 1.1.1: 0.28
    │   │   ├── 1.1.2: 0.42
    │   │   └── 1.1.3: 0.14
    │   ├── 1.2: 1.67
    │   │   ├── 1.2.1: 0.28
    │   │   ├── 1.2.2: 0.56
    │   │   └── 1.2.3: 0.83
    │   └── 1.3: 2.5
    │       ├── 1.3.1: 1.25
    │       ├── 1.3.2: 0.42
    │       └── 1.3.3: 0.83
    ├── 2: 1.67
    └── 3: 3.33
"""
        assert self.vt.get_tree_representation(node_info) == expected
        first_child.remove(first_child.get_children()[1])
        expected = """└── 0: 10.0
    ├── 1: 5.0
    │   ├── 1.1: 0.83
    │   │   ├── 1.1.1: 0.28
    │   │   ├── 1.1.2: 0.42
    │   │   └── 1.1.3: 0.14
    │   └── 1.2: 2.5
    │       ├── 1.2.1: 1.25
    │       ├── 1.2.2: 0.42
    │       └── 1.2.3: 0.83
    ├── 2: 1.67
    └── 3: 3.33
"""
        assert self.vt.get_tree_representation(node_info) == expected
        first_child.get_children()[0].change_value(2.5)
        expected = """└── 0: 10.0
    ├── 1: 5.0
    │   ├── 1.1: 2.5
    │   │   ├── 1.1.1: 0.83
    │   │   ├── 1.1.2: 1.25
    │   │   └── 1.1.3: 0.42
    │   └── 1.2: 2.5
    │       ├── 1.2.1: 1.25
    │       ├── 1.2.2: 0.42
    │       └── 1.2.3: 0.83
    ├── 2: 1.67
    └── 3: 3.33
"""

class WrongValueErrorTest(TestCase):
    pass