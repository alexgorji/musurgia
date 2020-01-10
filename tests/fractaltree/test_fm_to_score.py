import os
from unittest import TestCase

from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.fractaltree.fractalmusic import FractalMusic
from musurgia.testcomparefiles import TestCompareFiles

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):

    def setUp(self) -> None:
        self.fm = FractalMusic(quarter_duration=12, tree_permutation_order=(3, 1, 2), proportions=[1, 2, 3])
        self.fm.midi_generator.set_directions(1, 1, -1)
        self.fm.midi_generator.midi_range = [55, 72]

    def test_1(self):
        fm = self.fm
        fm.add_layer()

        fm.add_layer(lambda n: True if n.fractal_order > 1 else False)
        fm.add_layer(lambda n: True if n.fractal_order > 1 else False)
        fm.add_layer(lambda n: True if n.fractal_order > 1 else False)
        # for node in fm.traverse():
        #     node.chord.add_words(node.midi_generator.midi_range)
        fm.add_layer(lambda n: True if n.fractal_order > 1 else False)

        # for node in fm.traverse():
        #     node.chord.add_words(node.children_generated_midis)
        #     node.chord.add_words(node.midi_generator.directions, relative_y=30)
        #     node.chord.add_words(node.children_generated_midis)
        #     node.chord.add_words(node.permutation_order, relative_y=60)

        score = TreeScoreTimewise()
        score = fm.get_score(score, show_fractal_orders=False)

        text_path = path + '_test_1.txt'
        fm.write_infos(text_path)
        TestCompareFiles().assertTemplate(file_path=text_path)

        xml_path = path + '_test_1.xml'
        score.write(path=xml_path)
        TestCompareFiles().assertTemplate(file_path=xml_path)
