import os

from musurgia.fractaltree.fractalmusic import FractalMusic
from musurgia.agunittest import AGTestCase

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):
    def setUp(self) -> None:
        self.fm = FractalMusic(proportions=[1, 2, 3, 4], tree_permutation_order=[3, 1, 4, 2], duration=10.4)

    def test_1(self):
        self.fm.tempo = self.fm.find_best_tempo()
        self.assertEqual(self.fm.duration, 10.4)

    def test_2(self):
        self.fm.tempo = self.fm.find_best_tempo()
        self.assertEqual(self.fm.quarter_duration, 13)

    def test_3(self):
        self.fm.add_layer()
        for child in self.fm.get_children():
            best_tempo = child.find_best_tempo()
            child.tempo = best_tempo
        # print([leaf.quarter_duration for leaf in self.fm.get_children()])
        self.fm.round_leaves()
        result = [4.0, 1.0, 7.0, 2.0]
        self.assertEqual([child.quarter_duration for child in self.fm.get_children()], result)

    def test_4(self):
        self.fm.add_layer()
        for child in self.fm.get_children():
            best_tempo = child.find_best_tempo()
            child.tempo = best_tempo
        self.fm.round_leaves()
        xml_path = path + '_test_4.xml'
        score = self.fm.get_root_score()
        score.write(xml_path)
        self.assertCompareFiles(xml_path)
