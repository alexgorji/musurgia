from itertools import cycle

from musurgia.agunittest import AGTestCase
from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.chordfield.valuegenerator import ValueGeneratorGroup, ValueGenerator, ValueGeneratorTypeConflict


class Test(AGTestCase):
    def test_1(self):
        vg_1 = ValueGenerator(generator=cycle([2]), duration=5)
        vg_2 = ValueGenerator(generator=cycle([3]), duration=10)
        vgg = ValueGeneratorGroup(vg_1, vg_2)
        actual = [vg_1.position_in_group_duration, vg_2.position_in_group_duration]
        expected = [0, 5]
        self.assertEqual(expected, actual)

    def test_2(self):
        vg_1 = ValueGenerator(generator=cycle([2]), duration=5)
        vg_2 = ValueGenerator(generator=cycle([3]), duration=10)
        vgg = ValueGeneratorGroup(vg_1, vg_2)
        actual = vgg.__next__()
        expected = 2
        self.assertEqual(expected, actual)

    def test_3(self):
        vg_1 = ValueGenerator(generator=cycle([2]), duration=5)
        vg_2 = ValueGenerator(generator=cycle([3]), duration=10)
        vgg = ValueGeneratorGroup(vg_1, vg_2)
        actual = vgg(6)
        expected = 5
        self.assertEqual(expected, actual)

    def test_4(self):
        vg_1 = ValueGenerator(generator=cycle([2]), duration=5)
        vg_2 = ValueGenerator(generator=cycle([3]), duration=10)
        vgg = ValueGeneratorGroup(vg_1, vg_2)
        actual = vgg(5)
        expected = 5
        self.assertEqual(expected, actual)

    def test_5(self):
        vg_1 = ValueGenerator(generator=ArithmeticProgression(a1=0.2, an=1, s=5, correct_s=True), duration=10)
        vg_2 = ValueGenerator(generator=cycle([3]), duration=10)
        with self.assertRaises(ValueGeneratorTypeConflict):
            ValueGeneratorGroup(vg_1, vg_2)

    def test_6(self):
        vg_1 = ValueGenerator(generator=ArithmeticProgression(a1=0.2, an=1, correct_s=True), duration=10,
                              value_mode='duration')
        vg_2 = ValueGenerator(generator=ArithmeticProgression(an=0.2, a1=1, correct_s=True), duration=5,
                              value_mode='duration')
        vgg = ValueGeneratorGroup(vg_1, vg_2)
        actual = list(vgg)
        expected = []
        self.assertEqual(expected, actual)
