from unittest import TestCase, skip

from musurgia.random import Random, RandomPoolError


class TestRandom(TestCase):

    def test_pool_error(self):
        with self.assertRaises(RandomPoolError):
            Random(pool=3)

    def test_pool_none(self):
        r = Random(pool=None)
        with self.assertRaises(RandomPoolError):
            r.__next__()

    def test_periodicity_and_seed(self):
        pool = [1, 3, 2, 4, 5]
        r = Random(pool=pool, periodicity=2, seed=20)
        output = [r.__next__() for _ in range(20)]
        expected = [3, 2, 1, 5, 3, 1, 4, 3, 2, 4, 5, 3, 2, 4, 1, 5, 4, 1, 3, 5]
        self.assertEqual(expected, output)

    def test_duplication_removal_in_pool(self):
        pool = [1, 3, 2, 4, 5, 1, 1, 1, 1, 1, 1]
        r = Random(pool=pool, periodicity=0, seed=20)
        expected = [1, 3, 2, 4, 5]
        self.assertEqual(expected, r.pool)

    def test_periodicity_0(self):
        pool = [1, 3, 2, 4, 5, 6]
        r = Random(pool=pool, periodicity=0, seed=20)
        output = [r.__next__() for _ in range(20)]
        expected = [6, 6, 3, 2, 6, 6, 1, 2, 5, 3, 1, 4, 4, 1, 1, 3, 2, 4, 5, 4]
        self.assertEqual(expected, output)

    @skip
    def test_forbidden_list(self):
        self.fail()

    @skip
    def test_counter(self):
        self.fail()

    @skip
    def test_result(self):
        self.fail()

    @skip
    def test_periodicity_None(self):
        self.fail()
