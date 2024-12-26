from itertools import cycle
from pathlib import Path
from unittest import TestCase

from musicscore.layout import StaffLayout
from musicscore.midi import Midi
from musurgia.magicrandom import MagicRandom
from musurgia.tests.utils_for_tests import (
    XMLTestCase,
    create_test_fractal_relative_musical_tree,
    test_fractal_structur_list,
)
from musurgia.trees.musicaltree import (
    FractalDirectionIterator,
    FractalMusicalTree,
    MidiMusicalTree,
    RelativeMusicTree,
)
from musurgia.trees.timelinetree import TimelineDuration

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


class TestFractalDirectionIterator(TestCase):
    def test_fractal_direction_iterator(self):
        ft = FractalMusicalTree(
            duration=TimelineDuration(10),
            proportions=(1, 2, 3, 4),
            main_permutation_order=(3, 1, 4, 2),
            permutation_index=(1, 1),
        )
        ft.add_layer()
        fdi = FractalDirectionIterator(main_direction_cell=[1, -1], fractal_node=ft)
        self.assertEqual(fdi.get_main_directions(), [1, -1, 1, -1])
        self.assertEqual(fdi.get_directions(), [1, 1, -1, -1])


class TestRelativeFractalMusicalTree(XMLTestCase):
    def setUp(self):
        self.ft = create_test_fractal_relative_musical_tree()
        self.ft.get_chord_factory().show_metronome = True

    def test_default_direction_iterator(self):
        # self.ft.set_relative_midis()
        for node in self.ft.traverse():
            self.assertEqual(
                node.direction_iterator.get_main_directions(), [1, -1, 1, -1]
            )
        expected = """└── [1, 1, -1, -1]
    ├── [-1, -1, 1, 1]
    │   ├── []
    │   ├── [-1, -1, 1, 1]
    │   │   ├── []
    │   │   ├── []
    │   │   ├── []
    │   │   └── []
    │   ├── []
    │   └── [1, 1, -1, -1]
    │       ├── []
    │       ├── []
    │       ├── []
    │       └── []
    ├── []
    ├── [1, -1, 1, -1]
    │   ├── []
    │   ├── []
    │   ├── [-1, -1, 1, 1]
    │   │   ├── []
    │   │   ├── []
    │   │   ├── []
    │   │   └── []
    │   └── [1, -1, 1, -1]
    │       ├── []
    │       ├── []
    │       ├── []
    │       └── []
    └── [-1, 1, -1, 1]
        ├── [-1, -1, 1, 1]
        │   ├── []
        │   ├── []
        │   ├── []
        │   └── []
        ├── [1, 1, -1, -1]
        │   ├── []
        │   ├── []
        │   ├── []
        │   └── []
        ├── []
        └── []
"""
        self.assertEqual(
            self.ft.get_tree_representation(
                key=lambda node: node.direction_iterator.get_directions()
            ),
            expected,
        )

    def test_relative_fractal_musical_tree(self):
        score = self.ft.export_score()
        score.staff_layout = StaffLayout()
        score.staff_layout.staff_distance = 100
        score.get_quantized = True
        with self.file_path(path, "fractal_relative") as xml_path:
            score.export_xml(xml_path)

    def test_relative_fractat_musical_ziczac_tree(self):
        for node in self.ft.traverse():
            node.direction_iterator = cycle([-1, 1])
        self.ft.set_relative_midis()
        score = self.ft.export_score()
        score.staff_layout = StaffLayout()
        score.staff_layout.staff_distance = 100

        score.get_quantized = True
        with self.file_path(path, "fractal_relative_ziczac") as xml_path:
            score.export_xml(xml_path)

    def test_set_relatve_midis_again(self):
        expected = """└── 60
    ├── 68.0
    │   ├── 80.0
    │   ├── 76.0
    │   │   ├── 68.0
    │   │   ├── 71.0
    │   │   ├── 76.0
    │   │   └── 75.0
    │   ├── 68.0
    │   └── 70.0
    │       ├── 72.0
    │       ├── 75.0
    │       ├── 76.0
    │       └── 72.0
    ├── 80.0
    ├── 84.0
    │   ├── 76.0
    │   ├── 72.0
    │   ├── 80.0
    │   │   ├── 68.0
    │   │   ├── 72.0
    │   │   ├── 80.0
    │   │   └── 78.0
    │   └── 68.0
    │       ├── 76.0
    │       ├── 80.0
    │       ├── 72.0
    │       └── 84.0
    └── 68.0
        ├── 60.0
        │   ├── 68.0
        │   ├── 65.0
        │   ├── 60.0
        │   └── 61.0
        ├── 68.0
        │   ├── 66.0
        │   ├── 63.0
        │   ├── 62.0
        │   └── 66.0
        ├── 62.0
        └── 66.0
"""
        self.assertEqual(
            self.ft.get_tree_representation(
                key=lambda node: node.get_chord_factory().midis[0].value
            ),
            expected,
        )
        for node in self.ft.traverse():
            node.direction_iterator.reset()
        self.ft.set_relative_midis()
        self.assertEqual(
            self.ft.get_tree_representation(
                key=lambda node: node.get_chord_factory().midis[0].value
            ),
            expected,
        )
