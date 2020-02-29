from itertools import cycle

from musurgia.agunittest import AGTestCase
from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.chordfield.valuegenerator import ValueGenerator, NoDurationError, PositionError, CallConflict, \
    GeneratorHasNoNextError
from musurgia.interpolation import RandomInterpolation


class Test(AGTestCase):
    def test_1(self):
        vg = ValueGenerator(generator=ArithmeticProgression(a1=0.2, an=1, s=20, correct_s=True), duration=100)
        expected = 20
        actual = sum(list(vg))
        self.assertEqual(expected, actual)

    def test_2(self):
        with self.assertRaises(NoDurationError):
            vg = ValueGenerator(generator=ArithmeticProgression(a1=0.2, an=1, s=10, correct_s=True))
            vg.__next__()

    def test_3(self):
        vg = ValueGenerator(generator=ArithmeticProgression(a1=0.2, an=1, s=10, correct_s=True), duration=20,
                            value_mode='duration')
        expected = 20
        actual = sum(list(vg))
        self.assertEqual(expected, actual)

    def test_4(self):
        vg = ValueGenerator(generator=cycle([1]), duration=20)
        vg.position_in_duration = 20
        with self.assertRaises(PositionError):
            vg.__next__()

    def test_5(self):
        vg = ValueGenerator(generator=cycle([1]), duration=20)
        expected = 1
        actual = vg(19)
        self.assertEqual(expected, actual)

    def test_6(self):
        vg = ValueGenerator(generator=cycle([1]), duration=20)
        with self.assertRaises(PositionError):
            vg(20)

    def test_7(self):
        vg = ValueGenerator(generator=cycle([1]), duration=20)
        with self.assertRaises(PositionError):
            vg(20)

    def test_8(self):
        vg = ValueGenerator(generator=ArithmeticProgression(a1=0.2, an=1, s=10), duration=20)
        with self.assertRaises(CallConflict):
            vg(21)

    def test_9(self):
        vg = ValueGenerator(generator=RandomInterpolation(start=[1, 1, 2], end=[3, 4, 5], seed=10, duration=10),
                            duration=100)
        actual = [vg(x / 2) for x in range(20)]
        expected = [1, 2, 2, 1, 1, 2, 3, 1, 3, 2, 3, 2, 4, 3, 2, 3, 2, 5, 4, 5]
        self.assertEqual(expected, actual)

    def test_10(self):
        vg = ValueGenerator(generator=RandomInterpolation(start=[1, 1, 2], end=[3, 4, 5], seed=10, duration=10),
                            duration=100)
        with self.assertRaises(GeneratorHasNoNextError):
            vg.__next__()

