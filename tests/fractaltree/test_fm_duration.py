from fractions import Fraction
from unittest import TestCase

from musurgia.fractaltree.fractalmusic import FractalMusic


def get_infos(fm):
    return [fm.module_tempo, fm.score_tempo, fm.quarter_duration, fm.duration,
            fm.score_duration]


def print_infos(fm):
    print('module_tempo={}; score_tempo={}; quarter_duration={}; duration={}; score_duration={};'.format(
        *get_infos(fm)))


class Test(TestCase):
    def setUp(self) -> None:
        self.fm = FractalMusic(tree_permutation_order=[3, 1, 2], proportions=[1, 2, 3], duration=20)

    def test_1(self):
        # print_infos(self.fm)
        result = [60, 60, Fraction(20, 1), Fraction(20, 1), Fraction(20, 1)]
        self.assertEqual(get_infos(self.fm), result)

    def test_2(self):
        self.fm.duration = 10
        # print_infos(self.fm)
        result = [60, 60, Fraction(10, 1), Fraction(10, 1), Fraction(10, 1)]
        # print(get_infos(self.fm))
        self.assertEqual(get_infos(self.fm), result)

    def test_3(self):
        self.fm.duration = 10
        self.fm.score_tempo = 72
        # print_infos(self.fm)
        result = [60, 72, Fraction(10, 1), Fraction(10, 1), Fraction(25, 3)]
        # print(get_infos(self.fm))
        self.assertEqual(get_infos(self.fm), result)

    def test_4(self):
        self.fm.duration = 10
        self.fm.score_tempo = 72
        self.fm.module_tempo = 120
        # print_infos(self.fm)
        result = [120, 72, Fraction(20, 1), Fraction(10, 1), Fraction(50, 3)]
        # print(get_infos(self.fm))
        self.assertEqual(get_infos(self.fm), result)

    def test_5(self):
        self.fm.duration = 10
        self.fm.score_tempo = 72
        self.fm.module_tempo = 120
        self.fm.quarter_duration = 40
        # print_infos(self.fm)
        result = [120, 72, 40, Fraction(20, 1), Fraction(100, 3)]
        # print(get_infos(self.fm))
        self.assertEqual(get_infos(self.fm), result)

    def test_6(self):
        self.fm.duration = 10
        self.fm.score_tempo = 72
        self.fm.module_tempo = 120
        self.fm.quarter_duration = 40
        self.fm.duration = 20
        # print_infos(self.fm)
        result = [120, 72, Fraction(40, 1), Fraction(20, 1), Fraction(100, 3)]
        # print(get_infos(self.fm))
        self.assertEqual(get_infos(self.fm), result)

    def test_7(self):
        self.fm.duration = 10
        self.fm.score_tempo = 72
        self.fm.module_tempo = 120
        self.fm.quarter_duration = 40
        self.fm.duration = 20
        self.fm.module_tempo = 60
        # print_infos(self.fm)
        result = [60, 72, Fraction(20, 1), Fraction(20, 1), Fraction(50, 3)]
        # print(get_infos(self.fm))
        self.assertEqual(get_infos(self.fm), result)

    def test_8(self):
        self.fm.duration = 10
        self.fm.score_tempo = 72
        self.fm.module_tempo = 120
        self.fm.quarter_duration = 40
        self.fm.duration = 20
        self.fm.module_tempo = 60
        self.fm.score_tempo = 60
        # print_infos(self.fm)
        result = [60, 60, Fraction(20, 1), Fraction(20, 1), Fraction(20, 1)]
        # print(get_infos(self.fm))
        self.assertEqual(get_infos(self.fm), result)

    def test_9(self):
        self.fm.duration = 10
        self.fm.score_tempo = 72
        self.fm.module_tempo = 120
        self.fm.quarter_duration = 40
        self.fm.duration = 20
        self.fm.module_tempo = 60
        self.fm.score_tempo = 60
        self.fm.module_tempo = 120
        self.fm.score_tempo = 30
        self.fm.score_duration = 10
        # print_infos(self.fm)
        result = [120, 30, Fraction(5, 1), Fraction(5, 2), Fraction(10, 1)]
        # print(get_infos(self.fm))
        self.assertEqual(get_infos(self.fm), result)
