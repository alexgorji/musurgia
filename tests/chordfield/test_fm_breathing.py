import os
from itertools import cycle

from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from quicktions import Fraction

from musurgia.agunittest import AGTestCase
from musurgia.chordfield.chordfield import Breathe, ChordField
from musurgia.chordfield.valuegenerator import ValueGenerator
from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        self.fm = FractalMusic(quarter_duration=24, tempo=40)
        self.fm.add_layer()

    def test_1(self):
        selected_nodes = self.fm.get_children()[:2]
        proportions = (1, 3, 1, 5, 1)
        breakpoints = (1, Fraction(1, 7), 1)
        breathe = Breathe(quarter_duration=sum(node.quarter_duration for node in selected_nodes),
                          proportions=proportions, breakpoints=breakpoints)
        test_chord_field = ChordField(duration_generator=breathe.duration_generator.__deepcopy__())
        breathe.add_child(ChordField(midi_generator=ValueGenerator(cycle([60])), long_ending_mode='self_extend',
                                     short_ending_mode='self_shrink', quarter_duration=8))
        breathe.add_child(ChordField(midi_generator=ValueGenerator(cycle([61])), long_ending_mode='self_extend',
                                     short_ending_mode='self_shrink', quarter_duration=12))
