from itertools import cycle

from musurgia.agunittest import AGTestCase
from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.chordfield.valuegenerator import ValueGeneratorGroup, ValueGenerator
from musurgia.interpolation import Interpolation


class Test(AGTestCase):

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
        expected = 3
        self.assertEqual(expected, actual)

    def test_4(self):
        vg_1 = ValueGenerator(generator=cycle([2]), duration=5)
        vg_2 = ValueGenerator(generator=cycle([3]), duration=10)
        vgg = ValueGeneratorGroup(vg_1, vg_2)
        actual = vgg(5)
        expected = 3
        self.assertEqual(expected, actual)

    def test_6(self):
        vg_1 = ValueGenerator(generator=ArithmeticProgression(a1=0.2, an=1, correct_s=True), duration=10,
                              value_mode='duration')
        vg_2 = ValueGenerator(generator=ArithmeticProgression(an=0.2, a1=1, correct_s=True), duration=5,
                              value_mode='duration')
        vgg = ValueGeneratorGroup(vg_1, vg_2)
        actual = [round(float(x), 3) for x in vgg]
        expected = [0.208, 0.264, 0.319, 0.375, 0.431, 0.486, 0.542, 0.597, 0.653, 0.708, 0.764, 0.819, 0.875, 0.931,
                    0.986, 1.042, 1.042, 0.923, 0.804, 0.685, 0.565, 0.446, 0.327, 0.208]
        self.assertEqual(expected, actual)

    def test_7(self):
        vg_1 = ValueGenerator(generator=Interpolation(start=0.1, end=1), duration=5)
        vg_2 = ValueGenerator(generator=Interpolation(start=1, end=0.1), duration=5)
        vgg = ValueGeneratorGroup(vg_1, vg_2)
        print(float(vgg(6)))


        # actual = [round(float(x), 3) for x in vgg]
        # expected = [0.208, 0.264, 0.319, 0.375, 0.431, 0.486, 0.542, 0.597, 0.653, 0.708, 0.764, 0.819, 0.875, 0.931,
        #             0.986, 1.042, 1.042, 0.923, 0.804, 0.685, 0.565, 0.446, 0.327, 0.208]
        # self.assertEqual(expected, actual)
