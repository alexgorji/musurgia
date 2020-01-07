import os
from unittest import TestCase

from musurgia.fractaltree.fractalmusic import FractalMusic
from musurgia.testcomparefiles import TestCompareFiles

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.fm = FractalMusic(proportions=[1, 2, 3], tree_permutation_order=[3, 1, 2], quarter_duration=20)

    def test_1(self):
        self.fm.midi_generator.midi_range = [60, 72]
        self.fm.add_layer()
        self.fm.get_children()[0].midi_value = 80
        self.fm.add_layer()
        for node in self.fm.traverse():
            node.chord.add_lyric(node.fractal_order)
        score = self.fm.get_score()
        score.max_division = 7

        text_path = path + '_test_1.txt'
        self.fm.write_infos(text_path)
        TestCompareFiles().assertTemplate(file_path=text_path)

        xml_path = path + '_test_1.xml'
        score.write(path=xml_path)
        TestCompareFiles().assertTemplate(file_path=xml_path)

    def test_2(self):
        self.fm.midi_generator.midi_range = [60, 72]
        self.fm.midi_generator.set_directions(1, -1, 1)
        self.fm.add_layer()
        self.fm.get_children()[0].midi_value = 80

        split_nodes = self.fm.get_children()[0].split(1, 1)
        split_nodes[1].midi_value = 0

        self.fm.add_layer()

        for node in self.fm.traverse():
            node.chord.add_lyric(node.fractal_order)
        score = self.fm.get_score()
        score.max_division = 7

        text_path = path + '_test_2.txt'
        self.fm.write_infos(text_path)
        TestCompareFiles().assertTemplate(file_path=text_path)

        xml_path = path + '_test_2.xml'
        score.write(path=xml_path)
        TestCompareFiles().assertTemplate(file_path=xml_path)
