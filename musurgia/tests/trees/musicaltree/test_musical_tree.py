from pathlib import Path

from musurgia.tests.utils_for_tests import (
    XMLTestCase,
    test_fractal_structur_list,
)

from musurgia.trees.musicaltree import (
    MagicRandomTreeMidiGenerator,
    MusicalTree,
)

path = Path(__file__)


class TestMusicalTree(XMLTestCase):
    def setUp(self):
        self.mt = MusicalTree.create_tree_from_list(
            test_fractal_structur_list, "duration"
        )
        self.mt.get_chord_factory().show_metronome = True

    def test_musical_tree_root_chord(self):
        chord = self.mt.get_chord_factory().create_chord()
        self.assertEqual(
            chord.quarter_duration, self.mt.get_duration().get_quarter_duration()
        )
        self.assertEqual(chord.metronome, self.mt.get_duration().get_metronome())


class TestTreeMidiGenerator(XMLTestCase):
    def setUp(self):
        self.mt = MusicalTree.create_tree_from_list(
            test_fractal_structur_list, "duration"
        )
        self.mt.get_chord_factory().show_metronome = True

    def test_random_midis(self):
        MagicRandomTreeMidiGenerator(
            self.mt, pool=list(range(60, 85)), seed=10, periodicity=7
        ).set_musical_tree_midis()
        score = self.mt.export_score()
        score.get_quantized = True
        with self.file_path(path, "random") as xml_path:
            score.export_xml(xml_path)
