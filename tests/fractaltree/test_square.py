import os
from unittest import TestCase

from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.fractaltree.fractalmusicsquare import Square
from musurgia.testcomparefiles import TestCompareFiles

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.square = Square(duration=600, tree_permutation_order=[4, 1, 2, 3], proportions=[1, 2, 3, 4])
        for module in self.square.modules.values():
            module.module_tempo = 72
        score_tempi = [round(tempo) for tempo in ArithmeticProgression(a1=40, an=72, n=4)]
        for row in self.square.rows:
            for module in row.modules:
                score_tempo = score_tempi[row.number - 1]
                module.score_tempo = score_tempo

    def test_1(self):
        text_path = path + '_test_1.txt'
        self.square.write_infos(text_path=text_path, show_module_tempo=True, show_score_tempo=True,
                                show_quarter_durations=True)
        TestCompareFiles().assertTemplate(text_path)

    def test_2(self):
        text_path = path + '_test_2.txt'
        module = self.square.get_module(1, 1)
        module.duration = 3

        self.square.write_infos(text_path=text_path, show_module_tempo=True, show_score_tempo=True,
                                show_quarter_durations=True)
        TestCompareFiles().assertTemplate(text_path)

    def test_3(self):
        self.square.change_module_duration(1, 1, 3)

        text_path = path + '_test_3.txt'

        self.square.write_infos(text_path=text_path, show_module_tempo=True, show_score_tempo=True,
                                show_quarter_durations=True)

        TestCompareFiles().assertTemplate(text_path)

    def test_4(self):
        self.square = Square(duration=600, tree_permutation_order=[3, 4, 2, 1], proportions=[1, 2, 3, 4],
                             reading_direction='vertical')
        self.square.change_module_duration(1, 1, 3)

        text_path = path + '_test_4.txt'

        self.square.write_infos(text_path=text_path, show_module_tempo=True, show_score_tempo=True,
                                show_quarter_durations=True)
        orders = [module.permutation_order for module in self.square.get_all_modules()]
        result = [[4, 1, 2, 3], [3, 2, 1, 4], [1, 3, 4, 2], [2, 4, 3, 1], [2, 3, 1, 4], [1, 4, 2, 3], [4, 2, 3, 1],
                  [3, 1, 4, 2], [1, 4, 3, 2], [2, 3, 4, 1], [3, 1, 2, 4], [4, 2, 1, 3], [3, 2, 4, 1], [4, 1, 3, 2],
                  [2, 4, 1, 3], [1, 3, 2, 4]]

        self.assertEqual(orders, result)
