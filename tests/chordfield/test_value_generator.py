from itertools import cycle

from musurgia.agunittest import AGTestCase
from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.chordfield.valuegenerator import IterableValueGenerator, CallableValueGenerator, \
    ValueGeneratorTypeConflict, ValueGeneratorGroup
from musurgia.interpolation import RandomInterpolation


class Test(AGTestCase):
    def test_1(self):
        vg = IterableValueGenerator(generator=ArithmeticProgression(a1=0.2, an=1, correct_s=True), quarter_duration=10)
        self.assertEqual(10, sum(list(vg)))

    def test_2(self):
        vg = CallableValueGenerator(generator=RandomInterpolation(start=[1, 1, 2], end=[3, 4, 5], seed=10),
                                    quarter_duration=10)
        test_case = [vg(x / 2) for x in range(20)]
        expected = [1, 2, 2, 1, 1, 2, 3, 1, 3, 2, 3, 2, 4, 3, 2, 3, 2, 5, 4, 5]
        self.assertEqual(expected, test_case)

    def test_3(self):
        vg_1 = IterableValueGenerator(generator=ArithmeticProgression(a1=0.2, an=1, correct_s=True),
                                      duration=10)
        vg_2 = CallableValueGenerator(generator=RandomInterpolation(start=[1, 1, 2], end=[3, 4, 5], seed=10),
                                      quarter_duration=10)
        with self.assertRaises(ValueGeneratorTypeConflict):
            ValueGeneratorGroup(vg_1, vg_2)

    def test_4(self):
        vg_1 = IterableValueGenerator(generator=ArithmeticProgression(a1=0.2, an=1, correct_s=True),
                                      quarter_duration=10)
        vg_2 = IterableValueGenerator(generator=cycle([1]))

    def test_5(self):
        vg_2 = CallableValueGenerator(generator=cycle([1]))
        vg_1 = IterableValueGenerator(generator=ArithmeticProgression(a1=0.2, an=1, correct_s=True),
                                      quarter_duration=10)

    # def test_2(self):
    #     vg_1 = ValueGenerator(generator=ArithmeticProgression(a1=0.2, an=1, correct_s=True), quarter_duration=10)
    #     vg_2 = ValueGenerator(generator=ArithmeticProgression(an=0.2, a1=1, correct_s=True), quarter_duration=5)
    #     vgg = ValueGeneratorGroup(vg_1, vg_2)
    #     print(vgg.quarter_duration)
    #     print(vgg.value_generators)
