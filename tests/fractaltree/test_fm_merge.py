import os
from unittest import TestCase
from AGmusic.AGfractaltree.fractaltree import FractalTree, FractalMusic
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def test_1(self):
        ft = FractalTree(proportions=(1, 2, 3, 4, 5), tree_permutation_order=(3, 5, 1, 2, 4))
        ft.add_layer()
        # ft.add_layer()
        # print(ft.get_leaves(key=lambda leaf: leaf.index))
        # print(ft.get_leaves(key=lambda leaf: leaf.fractal_order))
        # print(ft.get_leaves(key=lambda leaf: round(float(leaf.value), 2)))
        ft.merge_children(1, 2, 2)
        # print(ft.get_leaves(key=lambda leaf: leaf.index))
        self.assertEqual(ft.get_leaves(key=lambda leaf: leaf.fractal_order), [3, 5, 2])
        self.assertEqual(ft.get_leaves(key=lambda leaf: round(float(leaf.value), 2)), [2.0, 4.0, 4.0])

    def test_2(self):
        fm = FractalMusic(proportions=(1, 2, 3, 4, 5), tree_permutation_order=(3, 5, 1, 2, 4))
        fm.midi_generator.midi_range = [60, 72]
        fm.add_layer()
        for ch in fm.get_children():
            ch.chord.add_words(ch.fractal_order)

        score = TreeScoreTimewise()
        fm.get_simple_format().to_stream_voice().add_to_score(score)

        fm.merge_children(2, 1, 2)
        # print(fm.get_leaves(key=lambda leaf: leaf.index))
        # print(fm.get_leaves(key=lambda leaf: leaf.fractal_order))
        # print(fm.get_leaves(key=lambda leaf: round(float(leaf.value), 2)))
        # print(fm.get_leaves(key=lambda leaf: round(float(leaf.duration), 2)))
        # print(fm.get_leaves(key=lambda leaf: round(float(leaf.chord.quarter_duration), 2)))
        fm.get_simple_format().to_stream_voice().add_to_score(score, part_number=2)
        xml_path = path + '_test_2.xml'
        score.write(xml_path)
        TestScore().assert_template(xml_path)
        # # ft.add_layer()
        # # print(ft.get_leaves(key=lambda leaf: leaf.index))
        # # print(ft.get_leaves(key=lambda leaf: leaf.fractal_order))
        # # print(ft.get_leaves(key=lambda leaf: round(float(leaf.value), 2)))
        # ft.merge_children(1, 2, 2)
        # # print(ft.get_leaves(key=lambda leaf: leaf.index))
        # self.assertEqual(ft.get_leaves(key=lambda leaf: leaf.fractal_order), [3, 5, 2])
        # self.assertEqual(ft.get_leaves(key=lambda leaf: round(float(leaf.value), 2)), [2.0, 4.0, 4.0])
