import os

from musurgia.agunittest import AGTestCase
from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.fractaltree.fractalmusicsquare import Square

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):
    def setUp(self) -> None:
        self.square = Square(duration=600, tree_permutation_order=[4, 1, 2, 3], proportions=[1, 2, 3, 4])
        # for module in self.square.modules.values():
        #     module.tempo = 72
        tempi = [round(tempo) for tempo in ArithmeticProgression(a1=40, an=72, n=4)]
        for row in self.square.rows:
            for module in row.modules:
                tempo = tempi[row.number - 1]
                module.tempo = tempo

    def test_1(self):
        text_path = path + '_test_1.txt'
        self.square.write_info(text_path=text_path, show_module_tempo=True, show_quarter_durations=True)
        self.assertCompareFiles(text_path)

    def test_2(self):
        text_path = path + '_test_2.txt'
        module = self.square.get_module(1, 1)
        module.duration = 3

        self.square.write_info(text_path=text_path, show_module_tempo=True,
                               show_quarter_durations=True)
        self.assertCompareFiles(text_path)

    def test_3(self):
        self.square.change_module_quarter_duration(1, 1, 3)

        text_path = path + '_test_3.txt'

        self.square.write_info(text_path=text_path, show_module_tempo=True,
                               show_quarter_durations=True)

        self.assertCompareFiles(text_path)

    def test_4(self):
        self.square = Square(duration=600, tree_permutation_order=[3, 4, 2, 1], proportions=[1, 2, 3, 4],
                             reading_direction='vertical')
        self.square.change_module_duration(1, 1, 3)

        orders = [module.permutation_order for module in self.square.get_all_modules()]
        result = [[4, 1, 2, 3], [3, 2, 1, 4], [1, 3, 4, 2], [2, 4, 3, 1], [2, 3, 1, 4], [1, 4, 2, 3], [4, 2, 3, 1],
                  [3, 1, 4, 2], [1, 4, 3, 2], [2, 3, 4, 1], [3, 1, 2, 4], [4, 2, 1, 3], [3, 2, 4, 1], [4, 1, 3, 2],
                  [2, 4, 1, 3], [1, 3, 2, 4]]

        self.assertEqual(result, orders)

    def test_5(self):
        row_1 = self.square.rows[0]
        row_1.change_module_duration(1, 3)
        text_path = path + '_test_5.txt'
        self.square.write_info(text_path=text_path, show_module_tempo=True,
                               show_quarter_durations=True)
        self.assertCompareFiles(text_path)

    def test_6(self):
        row_2 = self.square.rows[1]
        row_2.change_module_quarter_duration(2, 3)
        text_path = path + '_test_6.txt'
        self.square.write_info(text_path=text_path, show_module_tempo=True,
                               show_quarter_durations=True)
        self.assertCompareFiles(text_path)
