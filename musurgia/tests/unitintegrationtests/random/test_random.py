from unittest import TestCase, skip

from musurgia.random import Random, RandomPoolError, RandomPeriodicityError


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

    def test_periodicity_error(self):
        pool = [1, 3, 2, 4, 5, 6]
        with self.assertRaises(RandomPeriodicityError):
            Random(pool=pool, periodicity=-1, seed=20)

        with self.assertRaises(RandomPeriodicityError):
            Random(pool=pool, periodicity=1.6, seed=20)

    def test_forbidden_list(self):
        pool = [1, 3, 2, 4, 5, 6]
        forbidden_list = [2, 3, 1]
        r = Random(pool=pool, periodicity=4, seed=20, forbidden_list=forbidden_list)
        assert r.forbidden_list == forbidden_list
        previous_forbidden_list = r.forbidden_list[:]
        el1 = next(r)
        assert el1 not in previous_forbidden_list
        assert forbidden_list == r.forbidden_list == [2, 3, 1] + [el1]
        previous_forbidden_list = r.forbidden_list[:]
        el2 = next(r)
        assert el2 not in previous_forbidden_list
        assert forbidden_list == r.forbidden_list == [3, 1] + [el1, el2]
        previous_forbidden_list = r.forbidden_list[:]
        el3 = next(r)
        assert el3 not in previous_forbidden_list
        assert forbidden_list == r.forbidden_list == [1] + [el1, el2, el3]

    def test_seed(self):
        r = Random(pool=[1, 2, 3], periodicity=0, seed=1)
        assert r.seed == 1

    def test_counter(self):
        r = Random(pool=[1, 2, 3], periodicity=0, seed=1)
        assert r.counter == 0
        next(r)
        assert r.counter == 1

    @skip
    def test_result(self):
        self.fail()

    def test_periodicity_None(self):
        pool = [1, 2, 3]
        r = Random(pool=pool)
        assert r.periodicity == len(r.pool) - 2
        r = Random(pool=pool, periodicity=None)
        assert r.periodicity == len(r.pool) - 2
        r.pool = [1, 2, 3, 4]
        assert r.periodicity == len(r.pool) - 2
        r.pool = [1]
        assert r.periodicity == 0

        pool = [1, 2, 3]
        periodicity = 5
        r = Random(pool=pool, periodicity=5)
        assert r.periodicity == len(r.pool) - 1
        r.pool = [1, 2, 3, 4, 5, 6, 7]
        assert r.periodicity == periodicity
        r.pool = [1, 2, 3, 4]
        assert r.periodicity == len(r.pool) - 1
