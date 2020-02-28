import os
from itertools import cycle

from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.agunittest import AGTestCase
from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.chordfield.chordfield import ChordField, ChordFieldGroup
from musurgia.fractaltree.fractalmusic import FractalMusic
from musurgia.interpolation import Interpolation, RandomInterpolation

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        fm = FractalMusic(quarter_duration=20, tempo=80)
        fm.midi_generator.midi_range = [60, 84]
        fm.add_layer()
        sorted_children = sorted(fm.get_children(), key=lambda child: child.fractal_order)
        sorted_children[-1].chord_field = ChordField(duration_generator=ArithmeticProgression(a1=0.2, an=2),
                                                     midi_generator=Interpolation(start=84, end=60, duration=None,
                                                                                  key=lambda midi: round(midi * 2) / 2))

        score = fm.get_score(show_fractal_orders=True)
        xml_path = path + '_test_1.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        def add_chord_field(child):
            child.chord_field = ChordField(duration_generator=ArithmeticProgression(a1=0.2, an=2),
                                           midi_generator=Interpolation(start=child.midi_generator.midi_range[0],
                                                                        end=child.midi_generator.midi_range[1],
                                                                        duration=None,
                                                                        key=lambda
                                                                            midi: round(midi * 2) / 2),
                                           short_ending_mode='prolong')

        fm = FractalMusic(quarter_duration=20, tempo=80, proportions=[1, 2, 3, 4, 5],
                          tree_permutation_order=[3, 1, 5, 2, 4])
        fm.midi_generator.midi_range = [60, 84]
        fm.add_layer()
        sorted_children = sorted(fm.get_children(), key=lambda child: child.fractal_order)
        add_chord_field(sorted_children[-1])

        score = fm.get_score(show_fractal_orders=True)
        xml_path = path + '_test_2.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_3(self):
        # fields: midi_generators
        # group: duration_generator with __call__ RandomInterpolation
        cf_1 = ChordField(midi_generator=cycle([60, 61, 64, 66]))
        cf_2 = ChordField(midi_generator=cycle([72, 73, 74, 73, 72]), long_ending_mode='post')
        cfg = ChordFieldGroup(
            duration_generator=RandomInterpolation(start=[0.25, 0.25, 0.5], end=[0.5, 0.75, 1], seed=20))
        cfg.add_field(cf_1)
        cfg.add_field(cf_2)

        # fm = FractalMusic(quarter_duration=20, tempo=80)
        # fm.add_layer()
        # fm.get_children()[0].chord_field = cf_1
        # fm.get_children()[1].chord_field = cf_2

        # print(cf_1.__dict__)

        # score = fm.get_score()
        # xml_path = path + 'test_3.xml'
        # score.write(xml_path)
        # self.assertCompareFiles(xml_path)
    # def test_3(self):
    #     def group_children(*sizes):
    #         return slice_list(fm.get_children(), sizes)
    #
    #     def add_chord_field(group):
    #         group_quarter_duration = sum([node.chord.quarter_duration for node in group])
    #         if group_quarter_duration == 5:
    #             chord_field_group = ChordFieldGroup(duration_generator=cycle([0.2]))
    #         else:
    #             chord_field_group = ChordFieldGroup(duration_generator=cycle([Fraction(1, 7)]))
    #         chord_field_group.midi_generator = InterpolationGroup()
    #         for i in range(len(group)):
    #             node = group[i]
    #             copy_node = node.__deepcopy__()
    #             copy_node.add_layer()
    #             start_midis = [node.midi_value for node in copy_node.get_children()]
    #             try:
    #                 next_node = group[i + 1]
    #                 copy_node = next_node.__deepcopy__()
    #                 copy_node.add_layer()
    #                 end_midis = [node.midi_value for node in copy_node.get_children()]
    #             except IndexError:
    #                 end_midis = start_midis
    #             node.chord_field = ChordField()
    #             chord_field_group.add_field(node.chord_field)
    #             chord_field_group.midi_generator.add_interpolation(
    #                 RandomInterpolation(start=start_midis, end=end_midis))
    #         print([interpolation.__dict__ for interpolation in chord_field_group.midi_generator._interpolations])
    #
    #     fm = FractalMusic(quarter_duration=20, tempo=80, proportions=[1, 2, 3, 4, 5],
    #                       tree_permutation_order=[3, 1, 5, 2, 4])
    #     fm.midi_generator.midi_range = [60, 84]
    #     fm.add_layer()
    #     fm.quantize_children(1)
    #
    #     grouped_children = group_children(2, 3)
    #     for group in grouped_children:
    #         add_chord_field(group)
    #     score = fm.get_score()
    #     xml_path = path + '_test_3.xml'
    #     score.write(xml_path)
