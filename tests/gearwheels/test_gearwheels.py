from musurgia.agunittest import AGTestCase
from musurgia.gearwheels import GearWheels, Wheel


class Test(AGTestCase):
    def test_1(self):
        wh = Wheel(size=4, start=60)
        expected = [60, 64, 68, 72, 76]
        actual = wh.get_positions(number_of_cycles=5)
        self.assertEqual(expected, actual)

    def test_1(self):
        wh = Wheel(size=4, start=60)
        expected = [60, 64, 68, 72, 76]
        actual = wh.get_positions(number_of_cycles=5)
        self.assertEqual(expected, actual)

    # def test_1(self):
    #     gw = GearWheels(wheels=[Wheel(3), Wheel(4), Wheel(5)])
    #     expected = [3, 1, 1, 1, 2, 1, 1, 2, 3, 1, 2, 2, 1, 3, 1, 2, 1, 2, 2, 1, 2, 1, 3, 1, 2, 2, 1, 3, 2, 1, 1, 2, 1,
    #                 1, 1, 3]
    #     actual = gw.get_rhythm()
    #     self.assertEqual(actual, expected)
    #
    # def test_2(self):
    #     gw = GearWheels(wheels=[Wheel(3, 0), Wheel(4, 1), Wheel(5, 2)])
    #     print(gw.get_result())
