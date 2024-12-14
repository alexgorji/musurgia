from unittest import TestCase

from musurgia.timing.duration import Duration, convert_duration_to_quarter_duration_value
from musurgia.trees.chordtree import ChordTree
from musurgia.trees.timelinetree import TimelineTree
from musicscore.chord import Chord
from musicscore.metronome import Metronome
from musicscore.quarterduration import QuarterDuration


class ChordTreeTestCase(TestCase):
    def setUp(self):
        self.mt = ChordTree(duration=Duration(4))
    
    def test_init(self):
        self.assertEqual(self.mt.get_value(), 4)
        self.assertTrue(isinstance(self.mt, TimelineTree))

    def test_tree_chord(self):
        ch = self.mt.get_chord()
        self.assertTrue(isinstance(ch, Chord))
        with self.assertRaises(AttributeError):
            self.mt.chord = Chord(60, 2)

    def test_tree_chord_quarter_duration(self):
        self.mt.metronome = Metronome(120)
        self.mt.duration = Duration(4)
        ch = self.mt.get_chord()
        self.assertEqual(ch.quarter_duration, 8)


# class ChordTreeToScoreTestCase(TestCase):
#     def setUp(self):
#         self.mt = create_test_music_tree()

#     def test_music_tree_layers_to_score(self):
#         self.fail()

#     def test_updated_musictree_to_score(self):
#         self.fail()

    