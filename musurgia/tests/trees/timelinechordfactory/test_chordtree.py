from pathlib import Path
from unittest import TestCase

# from musicscore.score import Score

# from musurgia.tests.utils_for_tests import (
#     XMLTestCase,
#     create_test_valued_tree,
# )
from musurgia.trees.timelinetree import (
    SimpleTimelineChordFactory,
    TimelineDuration,
    TimelineTree,
)
from musicscore.chord import Chord
from musicscore.metronome import Metronome


class TimelineChordTreeTestCase(TestCase):
    def setUp(self):
        self.tlt = TimelineTree(duration=TimelineDuration(4))
        self.chf = SimpleTimelineChordFactory(self.tlt, show_metronome=True)

    def test_tree_chord(self):
        ch = self.chf.get_chord()
        self.assertTrue(isinstance(ch, Chord))
        with self.assertRaises(AttributeError):
            self.chf.chord = Chord(60, 2)
        self.assertEqual(ch.metronome.per_minute, 60)
        self.assertEqual(ch.quarter_duration, self.tlt.get_value())
        self.assertEqual(ch.midis[0].value, 72)

    def test_update_quarter_duration(self):
        self.assertEqual(self.tlt.get_duration().get_quarter_duration(), 4)
        self.tlt.get_duration().metronome = Metronome(120)
        self.assertEqual(self.chf.get_chord().quarter_duration, 8)
        self.tlt.update_duration(5)
        self.assertEqual(self.chf.get_chord().quarter_duration, 10)
        self.tlt.get_duration().metronome = Metronome(120, 2)
        self.tlt.metronome = Metronome(120, 2)
        self.assertEqual(self.chf.get_chord().quarter_duration, 20)


path = Path(__file__)


# class ChordTreeToScoreTestCase(XMLTestCase):
# def setUp(self):
#     self.mt = create_test_chord_tree()
#     self.vt = create_test_valued_tree()
#     self.score = Score()

# def test_tree_chord_quarter_durations(self):
#     mt_get_values = self.mt.get_tree_representation(
#         key=lambda node: node.get_value()
#     )
#     vt_get_values = self.mt.get_tree_representation(
#         key=lambda node: node.get_chord().quarter_duration.value
#     )
#     mt_get_durations = self.mt.get_tree_representation(
#         key=lambda node: node.get_duration().calculate_in_seconds()
#     )
#     mt_get_chord_quarter_durations = self.mt.get_tree_representation(
#         key=lambda node: node.get_chord().quarter_duration.value
#     )

#     assert mt_get_values == vt_get_values
#     assert vt_get_values == mt_get_durations
#     assert mt_get_durations == mt_get_chord_quarter_durations

# def test_valued_tree_layer_to_score(self):
#     for layer_number in range(self.vt.get_number_of_layers() + 1):
#         part = self.score.add_part(f"part-{layer_number + 1}")
#         layer = self.vt.get_layer(level=layer_number)
#         values = [node.get_value() for node in layer]
#         for val in values:
#             part.add_chord(Chord(quarter_duration=val, midis=[60]))

#     self.score.set_possible_subdivisions([2, 3, 4, 5, 6, 7, 8])
#     self.score.get_quantized = True
#     self.score.finalize()
#     with self.file_path(path, "valued_layers_to_score") as xml_path:
#         self.score.export_xml(xml_path)

# # There is a bug in musurgia (layer_number in range(1, 3) => musicscore.exceptions.AlreadyFinalizedError: Chord is already finalized.)
# def test_chord_tree_layers_to_score(self):
#     for layer_number in range(self.mt.get_number_of_layers() + 1):
#         part = self.score.add_part(f"part-{layer_number + 1}")
#         layer = self.mt.get_layer(level=layer_number)
#         for node in layer:
#             part.add_chord(node.get_chord())
#         print([id(ch) for ch in part.get_chords()])
#     #     print([chord.quarter_duration for chord in part.get_chords()])
#     self.score.set_possible_subdivisions([2, 3, 4, 5, 6, 7, 8])
#     self.score.get_quantized = True
#     self.score.finalize()
#     with self.file_path(path, "layers_to_score") as xml_path:
#         self.score.export_xml(xml_path)
