from pathlib import Path

from musicscore.midi import Midi
from musurgia.magicrandom import MagicRandom
from musurgia.tests.utils_for_tests import (
    XMLTestCase,
    create_test_fractal_relative_musical_tree,
    test_fractal_structur_list,
)
from musurgia.trees.musicaltree import MidiMusicalTree, RelativeMusicTree

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


class TestRandomMusicalTree(XMLTestCase):
    def setUp(self):
        self.mt = MidiMusicalTree.create_tree_from_list(
            test_fractal_structur_list, "duration"
        )
        self.mt.get_chord_factory().show_metronome = True

    def set_random_midis(self, musical_tree, root_midi_range, periodicitiy, seed):
        min_midi, max_midi = root_midi_range
        random_ = MagicRandom(
            pool=list(range(min_midi, max_midi + 1)),
            periodicity=periodicitiy,
            seed=seed,
        )
        for node in musical_tree.traverse():
            node.get_chord_factory().midis = [Midi(next(random_))]

    def test_random_midis(self):
        self.set_random_midis(
            musical_tree=self.mt, root_midi_range=(60, 84), seed=10, periodicitiy=7
        )
        score = self.mt.export_score()
        score.get_quantized = True
        with self.file_path(path, "random") as xml_path:
            score.export_xml(xml_path)


class TestRelativeMidiMusicalTree(XMLTestCase):
    def setUp(self):
        self.mt = RelativeMusicTree.create_tree_from_list(
            test_fractal_structur_list, "duration"
        )
        self.mt.midi_value_range = (60, 84)
        self.mt.get_chord_factory().show_metronome = True

    def test_relative_midis(self):
        self.mt.set_relative_midis()
        score = self.mt.export_score()
        score.get_quantized = True
        with self.file_path(path, "relative") as xml_path:
            score.export_xml(xml_path)


class TestRelativeFractalMusicalTree(XMLTestCase):
    def setUp(self):
        self.ft = create_test_fractal_relative_musical_tree()
        self.ft.get_chord_factory().show_metronome = True

    def test_relative_fractal_musical_tree(self):
        score = self.ft.export_score()
        score.get_quantized = True
        with self.file_path(path, "fractal_relative") as xml_path:
            score.export_xml(xml_path)
