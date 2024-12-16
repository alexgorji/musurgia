from pathlib import Path
from unittest import TestCase

from musicscore.score import Score

from musurgia.tests.utils_for_tests import XMLTestCase, create_test_chord_tree, create_test_valued_tree
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


path = Path(__file__)

class ChordTreeToScoreTestCase(XMLTestCase):
    def setUp(self):
        self.mt = create_test_chord_tree()
        self.vt = create_test_valued_tree()
        self.score = Score()

    # There is a bug in musurgia (layer_number in range(1, 3) => musicscore.exceptions.AlreadyFinalizedError: Chord is already finalized.)
    # Maybe There is a bug in musicscore: 
    # @skip
    def test_chord_tree_layers_to_score(self):
        # for layer_number in range(self.mt.get_number_of_layers() + 1):
        for layer_number in range(self.vt.get_number_of_layers() + 1):
            part = self.score.add_part(f"part-{layer_number + 1}")
            layer = self.vt.get_layer(level=layer_number)
            values = [node.get_value()for node in layer]
            print(values)
            for val in values:
                part.add_chord(Chord(quarter_duration=val, midis=[60]))
        #     for node in layer:
        #         part.add_chord(node.get_chord())
        #     print([chord.quarter_duration for chord in part.get_chords()])
        self.score.set_possible_subdivisions([2, 3, 4, 5, 6, 7, 8])
        self.score.get_quantized = True
        self.score.finalize()
        with self.file_path(path, 'layers_to_score') as xml_path:
            self.score.export_xml(xml_path)
