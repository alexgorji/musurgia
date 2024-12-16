# from unittest import TestCase

# from musurgia.timing.duration import Duration
# from musurgia.trees.chordtree import ChordFactory
# from musicscore.metronome import Metronome

# class ChordFactoryTestCase(TestCase):
#     def setUp(self):
#         self.chf = ChordFactory()
        
#     def test_default_chord(self):
#         self.assertEqual(self.chf.duration, 1)
#         self.assertEqual(self.chf.metronome.per_minute, 60)
#         self.assertEqual(self.chf.get_chord().quarter_duration, 1)
#         self.assertEqual(self.chf.get_chord().midis[0].value, 60)

#     def test_update_duration(self):
#         self.chf.duration.seconds = 2
#         self.assertEqual(self.chf.duration, 2)
#         self.assertEqual(self.chf.get_chord().quarter_duration, 2)

#         self.chf.duration = Duration(5)
#         self.assertEqual(self.chf.get_chord().quarter_duration, 5)

#     def test_update_metronome(self):
#         self.chf.metronome = Metronome(120, 2)
#         self.assertEqual(self.chf.get_chord().quarter_duration, 4)
