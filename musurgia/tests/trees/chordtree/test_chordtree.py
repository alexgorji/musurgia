# from unittest import TestCase

# from musurgia.timing.duration import Duration, convert_duration_to_quarter_duration_value
# from musurgia.trees.chordtree import ChordTree
# from musurgia.trees.timelinetree import TimelineTree
# from musicscore.chord import Chord
# from musicscore.metronome import Metronome
# from musicscore.quarterduration import QuarterDuration


# class ChordFactoryTestCase(TestCase):
#     def setUp(self):
#         self.chf = ChordFactory()

#     def test_update_duration(self):
#         self.chf.duration.seconds = 2
#         self.assertEqual(self.chf.duration, 2)
#         self.assertEqual(self.chf.get_chord().quarter_duration, 2)

#         self.chf.duration = Duration(5)
#         self.assertEqual(self.chf.get_chord().quarter_duration, 5)

#     def test_update_metronome(self):
#         self.chf.metronome = Metronome(120, 2)
#         self.assertEqual(self.chf.get_chord().quarter_duration, 4)

# class ChordTreeTestCase(TestCase):
#     def setUp(self):
#         self.mt = ChordTree(duration=Duration(4))

#     def test_init(self):
#         self.assertEqual(self.mt.get_value(), 4)
#         self.assertTrue(isinstance(self.mt, TimelineTree))

#     def test_tree_chord(self):
#         ch = self.mt.get_chord()
#         self.assertTrue(isinstance(ch, Chord))
#         with self.assertRaises(AttributeError):
#             self.mt.chord = Chord(60, 2)
#         self.assertEqual(ch.metronome.per_minute, 60)
#         self.assertEqual(ch.quarter_duration, self.mt.get_value())
#         self.assertEqual(ch.get_chord().midis[0].value, 60)

#     def test_tree_chord_update_quarter_duration(self):
#         self.mt.metronome = Metronome(120)
#         self.mt.duration = Duration(4)
#         ch = self.mt.get_chord()
#         self.assertEqual(ch.quarter_duration, 8)
#         self.assertEqual(self.chf.duration, 2)
#         self.assertEqual(self.chf.get_chord().quarter_duration, 2)

#         self.chf.duration = Duration(5)
#         self.assertEqual(self.chf.get_chord().quarter_duration, 5)


#         self.chf.metronome = Metronome(120, 2)
#         self.assertEqual(self.chf.get_chord().quarter_duration, 4)


# # class ChordTreeToScoreTestCase(TestCase):
# #     def setUp(self):
# #         self.mt = create_test_music_tree()

# #     def test_music_tree_layers_to_score(self):
# #         self.fail()

# #     def test_updated_musictree_to_score(self):
# #         self.fail()

