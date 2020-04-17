from unittest import TestCase

from musurgia.permutation import LimitedPermutation


class Test(TestCase):
    def test_1(self):
        perm = LimitedPermutation(['a', 'b', 'c'], [3, 1, 2], multi=[1, 1], reading_direction='horizontal')

        result = [[3, 1, 2], [2, 3, 1], [1, 2, 3], [1, 2, 3], [3, 1, 2], [2, 3, 1], [2, 3, 1], [1, 2, 3], [3, 1, 2]]
        self.assertEqual(result, perm.multiplied_orders)

    def test_2(self):
        perm = LimitedPermutation(['a', 'b', 'c'], [3, 1, 2], multi=[1, 1], reading_direction='horizontal')

        result = [[3, 1, 2], [2, 3, 1], [1, 2, 3], [1, 2, 3], [3, 1, 2], [2, 3, 1], [2, 3, 1], [1, 2, 3], [3, 1, 2]]
        self.assertEqual(result, perm.multiplied_orders)

    def test_3(self):
        perm = LimitedPermutation(['a', 'b', 'c'], [3, 1, 2], multi=[1, 1], reading_direction='vertical')

        result = [[1, 3, 2], [2, 1, 3], [3, 2, 1], [2, 1, 3], [3, 2, 1], [1, 3, 2], [3, 2, 1], [1, 3, 2], [2, 1, 3]]
        self.assertEqual(result, perm.multiplied_orders)


