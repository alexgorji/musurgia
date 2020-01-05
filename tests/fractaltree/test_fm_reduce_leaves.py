import os
from unittest import TestCase

from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore
from quicktions import Fraction

from AGmusic.AGfractaltree.fractaltree import FractalTree, FractalMusic

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def test_1_1(self):
        ft = FractalTree(proportions=(1, 2, 3), tree_permutation_order=(3, 1, 2))
        ft.add_layer()
        ft.add_layer()
        self.assertEqual([node.fractal_order for node in ft.traverse_leaves()], [1, 2, 3, 3, 1, 2, 2, 3, 1])

    def test_1_2(self):
        ft = FractalTree(proportions=(1, 2, 3), tree_permutation_order=(3, 1, 2))
        ft.add_layer()
        ft.add_layer()
        self.assertEqual([node.value for node in ft.traverse_leaves()],
                         [Fraction(5, 6), Fraction(5, 3), Fraction(5, 2), Fraction(5, 6), Fraction(5, 18),
                          Fraction(5, 9),
                          Fraction(10, 9), Fraction(5, 3), Fraction(5, 9)])

    def test_1_3(self):
        ft = FractalTree(proportions=(1, 2, 3), tree_permutation_order=(3, 1, 2))
        ft.add_layer()
        ft.add_layer()
        for node in ft.get_layer(1):
            node.reduce_children(condition=lambda node: node.fractal_order == 1)
        self.assertEqual([node.fractal_order for node in ft.traverse_leaves()], [2, 3, 3, 2, 2, 3])

    def test_1_4(self):
        ft = FractalTree(proportions=(1, 2, 3), tree_permutation_order=(3, 1, 2))
        ft.add_layer()
        ft.add_layer()
        for node in ft.get_layer(1):
            node.reduce_children(condition=lambda node: node.fractal_order == 1)
        self.assertEqual([node.value for node in ft.traverse_leaves()],
                         [Fraction(25, 12), Fraction(35, 12), Fraction(35, 36), Fraction(25, 36), Fraction(25, 18),
                          Fraction(35, 18)])

    def test_1(self):
        ft = FractalTree(proportions=(1, 2, 3), tree_permutation_order=(3, 1, 2))
        ft.add_layer()
        ft.add_layer()
        self.assertEqual([node.fractal_order for node in ft.traverse_leaves()], [1, 2, 3, 3, 1, 2, 2, 3, 1])
        self.assertEqual([node.value for node in ft.traverse_leaves()],
                         [Fraction(5, 6), Fraction(5, 3), Fraction(5, 2), Fraction(5, 6), Fraction(5, 18),
                          Fraction(5, 9),
                          Fraction(10, 9), Fraction(5, 3), Fraction(5, 9)])
        # ft.reduce_leaves(condition=lambda node: node.fractal_order == 1)
        for node in ft.get_layer(1):
            node.reduce_children(condition=lambda node: node.fractal_order == 1)
        self.assertEqual([node.fractal_order for node in ft.traverse_leaves()], [2, 3, 3, 2, 2, 3])
        self.assertEqual([node.value for node in ft.traverse_leaves()],
                         [Fraction(25, 12), Fraction(35, 12), Fraction(35, 36), Fraction(25, 36), Fraction(25, 18),
                          Fraction(35, 18)])

    def test_2(self):
        fm = FractalMusic(proportions=[1, 2, 3, 4], tree_permutation_order=[3, 1, 4, 2], quarter_duration=100)
        fm.midi_generator.midi_range = [60, 79]
        fm.add_layer()
        partial_fm = fm.get_leaves()[3]
        partial_fm.add_layer()
        for leaf in partial_fm.traverse():
            leaf.chord.add_lyric(leaf.fractal_order)
            leaf.chord.add_words(leaf.midi_generator.midi_range)
            # leaf.chord.add_words(leaf.midi_generator.directions, relative_y=30)
        # print([leaf.fractal_order for leaf in partial_fm.traverse_leaves()])
        score = TreeScoreTimewise()
        v = partial_fm.get_simple_format(0).to_stream_voice(1)
        v.add_to_score(score, 1, 1)

        v = partial_fm.get_simple_format().__deepcopy__().to_stream_voice(1)
        v.add_to_score(score, 1, 2)

        partial_fm.reduce_children(condition=lambda child: child.fractal_order > 2)
        v = partial_fm.get_simple_format().__deepcopy__().to_stream_voice(1)
        v.add_to_score(score, 1, 3)

        result_path = path + '_test_2'
        score.write(result_path)
        TestScore().assert_template(result_path=result_path)

    # def test_3(self):
    #     fm = FractalMusic(proportions=[1, 2, 3, 4], tree_permutation_order=[3, 1, 4, 2], duration=100)
    #     fm.midi_generator.midi_range = [60, 79]
    #     fm.midi_generator.directions = [1, 1, -1]
    #     fm.add_layer()
    #     print(fm.children_generated_midis)
    #     print(fm.children_fractal_values)
    #     fm.reduce_children(lambda child: child.fractal_order == 2)
    #     print(fm.children_fractal_values)
    #     print(fm.midi_generator.proportions)
    #     print(fm.midi_generator.directions)
    #     print(fm.children_generated_midis)
    #     print(fm.proportions)
    #     fm.add_layer()
    #     print([leaf.fractal_order for leaf in fm.traverse_leaves()])

    # print([leaf.fractal_order for leaf in fm.traverse_leaves()])
    #
    # fm.reduce_leaves(lambda leaf: leaf.fractal_order == 2)
    # print([leaf.midi_value for leaf in fm.traverse_leaves()])

    # def test_4(self):
    #     permutation_order = [8, 11, 7, 12, 10, 13, 9, 4, 1, 3, 6, 2, 5]
    #     fm = FractalMusic(tree_permutation_order=permutation_order, duration=900, proportions=list(range(1, 14)))
    #     fm.midi_generator.midi_range = [48, 84]
    #     fm.midi_generator.directions = [1, 1, -1, -1]
    #     fm.add_layer()
    #     part_fm = fm.get_children()[6]
    #     part_fm.add_layer()
    #     print([child.fractal_order for child in part_fm.get_children()])
    #     part_fm.reduce_children(lambda child: child.fractal_order < 5)
    #     print([child.fractal_order for child in part_fm.get_children()])
    #     print([round(float(duration), 2) for duration in part_fm.simple_format.durations])

    # fm.reduce_leaves(lambda leaf: leaf.fractal_order == 2)

    def test_5(self):
        score = TreeScoreTimewise()

        fm = FractalMusic(proportions=[1, 2, 3, 4], tree_permutation_order=[3, 1, 4, 2], quarter_duration=20)
        fm.midi_generator.midi_range = [60, 79]
        fm.midi_generator.microtone = 4
        fm.add_layer()

        for child in fm.get_children():
            child.chord.add_lyric(child.fractal_order)

        simple_format = fm.get_simple_format(1)
        v = simple_format.to_stream_voice(1)
        v.add_to_score(score, 1, 1)

        fm.reduce_children(lambda child: child.fractal_order in [1])

        simple_format = fm.get_simple_format(1)
        v = simple_format.to_stream_voice(1)
        v.add_to_score(score, 1, 2)

        fm.add_layer()

        for leaf in fm.traverse_leaves():
            leaf.chord.add_lyric(leaf.fractal_order)
            # leaf.chord.add_words(leaf.midi_generator.midi_range[1])

        simple_format = fm.get_simple_format(2)
        v = simple_format.to_stream_voice(1)
        v.add_to_score(score, 1, 3)



        result_path = path + '_test_5'
        file_name = result_path + '.txt'
        fm.write_infos(file_name)
        score.max_division = 7
        score.write(result_path)
        TestScore().assert_template(result_path=result_path)
