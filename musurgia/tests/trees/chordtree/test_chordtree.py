from unittest import TestCase

from musurgia.trees.chordtree import ChordTree
from musurgia.trees.timelinetree import TimelineDuration, TimelineTree
from musicscore.chord import Chord
from musicscore.metronome import Metronome


class ChordTreeTestCase(TestCase):
    def setUp(self):
        self.cht = ChordTree(duration=TimelineDuration(4))

    def test_init(self):
        self.assertEqual(self.cht.get_value(), 4)
        self.assertTrue(isinstance(self.cht, TimelineTree))

    def test_tree_chord(self):
        ch = self.cht.get_chord()
        self.assertTrue(isinstance(ch, Chord))
        with self.assertRaises(AttributeError):
            self.cht.chord = Chord(60, 2)
        self.assertEqual(ch.metronome.per_minute, 60)
        self.assertEqual(ch.quarter_duration, self.cht.get_value())
        self.assertEqual(ch.midis[0].value, 60)

    def test_tree_chord_update_quarter_duration(self):
        self.cht.metronome = Metronome(120)
        self.cht.update_duration(TimelineDuration(4))
        ch = self.cht.get_chord()
        self.assertEqual(ch.quarter_duration, 8)
        self.assertEqual(self.cht.get_duration(), 4)

        self.cht.update_duration(TimelineDuration(5))
        self.assertEqual(self.cht.get_chord().quarter_duration, 10)

        self.cht.metronome = Metronome(120, 2)
        self.assertEqual(self.cht.get_chord().quarter_duration, 20)


# class ChordTreeToScoreTestCase(TestCase):
#     def setUp(self):
#         self.mt = create_test_music_tree()

#     def test_music_tree_layers_to_score(self):
#         self.fail()

#     def test_updated_musictree_to_score(self):
#         self.fail()
