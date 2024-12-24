from pathlib import Path
from musurgia.tests.utils_for_tests import XMLTestCase, test_fractal_structur_list
from musurgia.trees.musicaltree import MidiMusicalTree

path = Path(__file__)


class TestSimpleMusicalTree(XMLTestCase):
    def setUp(self):
        self.mt = MidiMusicalTree.create_tree_from_list(
            test_fractal_structur_list, "duration"
        )
        self.mt.get_chord_factory().show_metronome = True

    def test_simple_music_tree_root_chord(self):
        chord = self.mt.get_chord_factory().create_chord()
        self.assertEqual(
            chord.quarter_duration, self.mt.get_duration().get_quarter_duration()
        )
        self.assertEqual(chord.metronome, self.mt.get_duration().get_metronome())

    def test_simple_music_tree_to_score(self):
        score = self.mt.export_score()
        score.get_quantized = True
        with self.file_path(path, "simple") as xml_path:
            score.export_xml(xml_path)


