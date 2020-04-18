from musurgia.agunittest import AGTestCase
from musurgia.gearwheels import GearWheels


class Test(AGTestCase):
    def test_1(self):
        gw = GearWheels(gear_sizes=[3, 4, 5])
        expected = [3, 1, 1, 1, 2, 1, 1, 2, 3, 1, 2, 2, 1, 3, 1, 2, 1, 2, 2, 1, 2, 1, 3, 1, 2, 2, 1, 3, 2, 1, 1, 2, 1,
                    1, 1, 3]
        actual = gw.get_rhythm()
        self.assertEqual(actual, expected)
