import os

from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.agunittest import AGTestCase
from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        xml_path = path + '_test_1.xml'
        fm = FractalMusic(tempo=60, quarter_duration=10)
        fm.midi_generator.midi_range = [60, 71]
        copied = fm.__deepcopy__()
        fm.add_layer()
        copied.tree_permutation_order = list(reversed(copied.tree_permutation_order))
        copied.add_layer()
        fm.add_info('fractal_order')
        copied.add_info('fractal_order')
        fm.get_simple_format().to_stream_voice().add_to_score(score=self.score, staff_number=1)
        copied.get_simple_format().to_stream_voice().add_to_score(score=self.score, staff_number=2)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        xml_path = path + '_test_2.xml'
        fm = FractalMusic(tempo=60, quarter_duration=10, reading_direction='vertical')
        fm.midi_generator.midi_range = [60, 71]
        copied = fm.__deepcopy__()
        fm.add_layer()
        print(fm.get_leaves(key=lambda leaf: leaf.fractal_order))
        copied.tree_permutation_order = list(reversed(copied.tree_permutation_order))
        copied.add_layer()
        print(copied.get_leaves(key=lambda leaf: leaf.fractal_order))
        fm.add_info('fractal_order')
        copied.add_info('fractal_order')
        fm.get_simple_format().to_stream_voice().add_to_score(score=self.score, staff_number=1)
        copied.get_simple_format().to_stream_voice().add_to_score(score=self.score, staff_number=2)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_3(self):
        xml_path = path + '_test_3.xml'
        fm = FractalMusic(tempo=60, quarter_duration=20, proportions=[1, 2, 3, 4, 5, 6],
                          tree_permutation_order=[4, 1, 5, 3, 6, 2], reading_direction='vertical')
        fm.midi_generator.midi_range = [60, 71]
        copied = fm.__deepcopy__()

        fm.add_layer()
        copied.tree_permutation_order = list(reversed(copied.tree_permutation_order))
        copied.add_layer()
        fm.add_info('fractal_order')
        copied.add_info('fractal_order')
        fm.get_simple_format().to_stream_voice().add_to_score(score=self.score, staff_number=1)
        copied.get_simple_format().to_stream_voice().add_to_score(score=self.score, staff_number=2)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
