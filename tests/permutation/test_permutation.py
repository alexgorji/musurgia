from unittest import TestCase
from musurgia.permutation import LimitedPermutation, self_permute, get_self_multiplied_permutation, \
    get_reordered_self_multiplied_permutation, get_vertical_self_multiplied_permutation


class Test(TestCase):
    def test_1_1(self):
        permutation_order = [3, 1, 2]
        self_permutation = self_permute(permutation_order)
        result = [[3, 1, 2], [2, 3, 1], [1, 2, 3]]
        self.assertEqual(self_permutation, result)

    def test_1_2(self):
        permutation_order = [3, 1, 2]
        self_multiplied_permutation = get_self_multiplied_permutation(permutation_order)
        result = [[[1, 2, 3], [3, 1, 2], [2, 3, 1]],
                  [[2, 3, 1], [1, 2, 3], [3, 1, 2]],
                  [[3, 1, 2], [2, 3, 1], [1, 2, 3]]]
        self.assertEqual(self_multiplied_permutation, result)

    def test_1_3(self):
        permutation_order = [3, 1, 2]
        reordered_self_multiplied_permutation = get_reordered_self_multiplied_permutation(permutation_order)
        result = [[[3, 1, 2], [2, 3, 1], [1, 2, 3]],
                  [[1, 2, 3], [3, 1, 2], [2, 3, 1]],
                  [[2, 3, 1], [1, 2, 3], [3, 1, 2]]]
        self.assertEqual(reordered_self_multiplied_permutation, result)

    def test_1_4(self):
        permutation_order = [3, 1, 2]
        vertical_self_multiplied_permutation = get_vertical_self_multiplied_permutation(permutation_order)
        result = [[[1, 3, 2], [2, 1, 3], [3, 2, 1]],
                  [[2, 1, 3], [3, 2, 1], [1, 3, 2]],
                  [[3, 2, 1], [1, 3, 2], [2, 1, 3]]]
        self.assertEqual(vertical_self_multiplied_permutation, result)

    def test_2_1(self):
        perm = LimitedPermutation(['a', 'b', 'c'], [3, 1, 2], multi=[1, 1])
        result = [[3, 1, 2], [2, 3, 1], [1, 2, 3], [1, 2, 3], [3, 1, 2], [2, 3, 1], [2, 3, 1], [1, 2, 3], [3, 1, 2]]
        self.assertEqual(perm.multiplied_orders, result)

    def test_2_2(self):
        perm = LimitedPermutation(['a', 'b', 'c'], [3, 1, 2], multi=[1, 1], reading_direction='vertical')

        result = [[1, 3, 2], [2, 1, 3], [3, 2, 1], [2, 1, 3], [3, 2, 1], [1, 3, 2], [3, 2, 1], [1, 3, 2], [2, 1, 3]]
        self.assertEqual(perm.multiplied_orders, result)

    def test_3_1(self):
        permutation_order = [3, 4, 2, 1]
        self_multiplied_permutation = get_self_multiplied_permutation(permutation_order)
        result = [[[4, 3, 1, 2], [1, 2, 3, 4], [2, 1, 4, 3], [3, 4, 2, 1]],
                  [[2, 1, 4, 3], [3, 4, 2, 1], [1, 2, 3, 4], [4, 3, 1, 2]],
                  [[1, 2, 3, 4], [4, 3, 1, 2], [3, 4, 2, 1], [2, 1, 4, 3]],
                  [[3, 4, 2, 1], [2, 1, 4, 3], [4, 3, 1, 2], [1, 2, 3, 4]]]
        self.assertEqual(self_multiplied_permutation, result)

    def test_3_2(self):
        permutation_order = [3, 4, 2, 1]
        reordered_self_multiplied_permutation = get_reordered_self_multiplied_permutation(permutation_order)
        result = [[[3, 4, 2, 1], [2, 1, 4, 3], [4, 3, 1, 2], [1, 2, 3, 4]],
                  [[4, 3, 1, 2], [1, 2, 3, 4], [2, 1, 4, 3], [3, 4, 2, 1]],
                  [[2, 1, 4, 3], [3, 4, 2, 1], [1, 2, 3, 4], [4, 3, 1, 2]],
                  [[1, 2, 3, 4], [4, 3, 1, 2], [3, 4, 2, 1], [2, 1, 4, 3]]]
        self.assertEqual(reordered_self_multiplied_permutation, result)

    def test_3_3(self):
        permutation_order = [3, 4, 2, 1]
        vertical_self_multiplied_permutation = get_vertical_self_multiplied_permutation(permutation_order)
        result = [[[4, 1, 2, 3], [3, 2, 1, 4], [1, 3, 4, 2], [2, 4, 3, 1]],
                  [[2, 3, 1, 4], [1, 4, 2, 3], [4, 2, 3, 1], [3, 1, 4, 2]],
                  [[1, 4, 3, 2], [2, 3, 4, 1], [3, 1, 2, 4], [4, 2, 1, 3]],
                  [[3, 2, 4, 1], [4, 1, 3, 2], [2, 4, 1, 3], [1, 3, 2, 4]]]
        self.assertEqual(vertical_self_multiplied_permutation, result)



