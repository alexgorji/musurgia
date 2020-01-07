from unittest import TestCase
from musurgia.permutation import LimitedPermutation


class Test(TestCase):
    def test_1(self):
        perm = LimitedPermutation(['a', 'b', 'c', 'c'], [3, 1, 4, 2], multi=[1, 1])
        result = [[3, 1, 4, 2], [4, 3, 2, 1], [2, 4, 1, 3], [1, 2, 3, 4], [2, 4, 1, 3], [3, 1, 4, 2], [1, 2, 3, 4],
                  [4, 3, 2, 1], [1, 2, 3, 4], [2, 4, 1, 3], [4, 3, 2, 1], [3, 1, 4, 2], [4, 3, 2, 1], [1, 2, 3, 4],
                  [3, 1, 4, 2], [2, 4, 1, 3]]
        self.assertEqual(perm.multiplied_orders, result)

    def test_2(self):
        perm = LimitedPermutation(['a', 'b', 'c', 'c'], [3, 1, 4, 2], multi=[1, 1])
        result = [[3, 1, 4, 2], [4, 3, 2, 1], [2, 4, 1, 3], [1, 2, 3, 4], [2, 4, 1, 3], [3, 1, 4, 2], [1, 2, 3, 4],
                  [4, 3, 2, 1], [1, 2, 3, 4], [2, 4, 1, 3], [4, 3, 2, 1], [3, 1, 4, 2], [4, 3, 2, 1], [1, 2, 3, 4],
                  [3, 1, 4, 2], [2, 4, 1, 3]]
        self.assertEqual(perm.multiplied_orders, result)
        perm.reading_direction = 'vertical'
        result = [[3, 4, 2, 1], [1, 3, 4, 2], [4, 2, 1, 3], [2, 1, 3, 4], [2, 3, 1, 4], [4, 1, 2, 3], [1, 4, 3, 2],
                  [3, 2, 4, 1], [1, 2, 4, 3], [2, 4, 3, 1], [3, 1, 2, 4], [4, 3, 1, 2], [4, 1, 3, 2], [3, 2, 1, 4],
                  [2, 3, 4, 1], [1, 4, 2, 3]]
        self.assertEqual(perm.multiplied_orders, result)
