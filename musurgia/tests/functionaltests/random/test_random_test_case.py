from unittest import TestCase

from musurgia.random import Random


class RandomTestCaseTest(TestCase):
    """
    To be sure that in a test case random object is set back for each test
    """

    def setUp(self) -> None:
        pool = [1, 2, 3, 4, 5]
        seed = 10
        periodicity = 2
        self.r = Random(pool=pool, seed=seed, periodicity=periodicity)
        self.first_ones = [next(self.r) for _ in range(5)]

    def test_dummy_1(self):
        assert self.first_ones == [5, 1, 4, 5, 1]
        assert [next(self.r) for _ in range(10)] == [2, 4, 3, 2, 1, 5, 4, 3, 1, 2]
        assert self.first_ones == [5, 1, 4, 5, 1]

    def test_dummy_2(self):
        assert self.first_ones == [5, 1, 4, 5, 1]
        assert [next(self.r) for _ in range(10)] == [2, 4, 3, 2, 1, 5, 4, 3, 1, 2]
        assert self.first_ones == [5, 1, 4, 5, 1]

    def test_dummy_3(self):
        assert self.first_ones == [5, 1, 4, 5, 1]
        assert [next(self.r) for _ in range(10)] == [2, 4, 3, 2, 1, 5, 4, 3, 1, 2]
        assert self.first_ones == [5, 1, 4, 5, 1]
