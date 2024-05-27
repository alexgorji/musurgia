from unittest import TestCase

from musurgia.permutation.permutation import permute


class TestPermutation(TestCase):
    def test_simple_permute(self):
        # wrong lengths
        with self.assertRaises(TypeError):
            permute([10, 20, 30, 40], (3, 2, 4))
        with self.assertRaises(TypeError):
            permute([10, 20, 30, 40], (3, 2, 4, 1, 3))
        # wrong orders
        with self.assertRaises(TypeError):
            permute([10, 20, 30, 40], (3, 2, 4, 5))

        with self.assertRaises(ValueError):
            permute([10, 20, 30, 40], (2, 3, 1))

        with self.assertRaises(ValueError):
            permute([10, 20, 30, 40], (2, 3, 1, 4, 5))

        assert permute([10, 20, 30, 40], (3, 2, 4, 1)) == [30, 20, 40, 10]
