from fractions import Fraction
import math
from unittest import TestCase

from musicscore.util import xToD

from musurgia.utils import Normalizer, RelativeValueGenerator


class NormalizeTestCase(TestCase):
    def test_normalize_value_to_itself(self):
        normalize = Normalizer(normalization_range=(1, 5), input_value_range=(1, 5))
        for x in [1, 3, 5]:
            self.assertEqual(normalize.get_normalized_value(x), x)

    def test_normalize_value_to_itself_out_of_range(self):
        normalize = Normalizer(normalization_range=(1, 5), input_value_range=(1, 5))
        for x in [-2, 0, 1, 5, 7]:
            self.assertEqual(normalize.get_normalized_value(x), x)

    def test_normalize_value(self):
        normalize = Normalizer(normalization_range=(0, 1), input_value_range=(0, 10))
        for x in [0, 3, 5, 8, 10]:
            self.assertEqual(normalize.get_normalized_value(x), Fraction(x, 10))

    def test_normalize_value_out_of_range(self):
        normalize = Normalizer(normalization_range=(0, 1), input_value_range=(0, 10))
        for x in [-3, -2, 0, 10, 13, 15]:
            self.assertEqual(normalize.get_normalized_value(x), Fraction(x, 10))


class RelativeValueGeneratorTestCase(TestCase):
    def setUp(self):
        self.rvr = RelativeValueGenerator(
            value_range=(1, 10),
            value_grid=None,
            directions=[-1, -1, 1, 1],
            proportions=[2, 4, 3, 2],
        )

    def _get_directions(self, input_list):
        directions = []
        for index, x in enumerate(input_list[1:]):
            previous = input_list[index]
            if x > previous:
                directions.append(1)
            elif x < previous:
                directions.append(-1)
            else:
                directions.appedn(0)
        return directions

    def _get_proportions(self, input_list):
        intervals = xToD(input_list)
        factor = math.lcm(*[x.denominator for x in intervals])
        non_fraction_intervals = [factor * interval for interval in intervals]
        integer_intervals = [x.numerator for x in non_fraction_intervals]
        assert integer_intervals == non_fraction_intervals
        gcd = math.gcd(*integer_intervals)
        return [abs(x / gcd) for x in integer_intervals]

    def test_init(self):
        self.assertEqual(self.rvr.value_range, (1, 10))
        self.assertIsNone(self.rvr.value_grid)
        self.assertEqual(self.rvr.directions, [-1, -1, 1, 1])
        self.assertEqual(self.rvr.proportions, [2, 4, 3, 2])
        relative_values = self.rvr.get_values()
        self.assertListEqual(
            relative_values,
            [
                Fraction(10, 1),
                Fraction(7, 1),
                Fraction(1, 1),
                Fraction(11, 2),
                Fraction(17, 2),
            ],
        )
        self.assertListEqual(self._get_directions(relative_values), self.rvr.directions)
        self.assertEqual(min(relative_values), self.rvr.value_range[0])
        self.assertEqual(max(relative_values), self.rvr.value_range[1])
        self.assertListEqual(
            self._get_proportions(relative_values), self.rvr.proportions
        )
