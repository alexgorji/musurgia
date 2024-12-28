from itertools import cycle
from pathlib import Path
from unittest import TestCase

from musicscore.layout import StaffLayout
from musurgia.tests.utils_for_tests import (
    XMLTestCase,
    create_test_fractal_relative_musical_tree,
    test_fractal_structur_list,
)

from musurgia.trees.musicaltree import (
    FractalDirectionIterator,
    FractalMusicalTree,
    FractalRelativeMusicTree,
    MagicRandomTreeMidiGenerator,
    MusicalTree,
    RelativeMusicTree,
    RelativeTreeChordFactory,
    RelativeTreeMidiGenerator,
)
from musurgia.trees.timelinetree import TimelineDuration

path = Path(__file__)


class TestMusicalTree(XMLTestCase):
    def setUp(self):
        self.mt = MusicalTree.create_tree_from_list(
            test_fractal_structur_list, "duration"
        )
        self.mt.get_chord_factory().show_metronome = True

    def test_simple_music_tree_root_chord(self):
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
        MagicRandomTreeMidiGenerator(self.mt, pool=list(range(60, 85)), seed=10, periodicity=7).set_musical_tree_midis()
        score = self.mt.export_score()
        score.get_quantized = True
        with self.file_path(path, "random") as xml_path:
            score.export_xml(xml_path)

class TestRelativeMusicalTree(XMLTestCase):
    def setUp(self):
        self.mt = RelativeMusicTree.create_tree_from_list(
            test_fractal_structur_list, "duration"
        )
        self.mt.get_chord_factory().show_metronome = True
        self.mt.get_chord_factory().midi_value_range=(60, 84)

    def test_chord_factory(self):
        self.assertTrue(self.mt.get_chord_factory(), RelativeTreeChordFactory)
        rtm = RelativeTreeMidiGenerator(musical_tree_node=self.mt)
        self.assertEqual(rtm.get_musical_tree_node(), self.mt)
        self.assertTrue(rtm.get_musical_tree_node().get_chord_factory(), RelativeTreeChordFactory)


    def test_relative_midis(self):
        RelativeTreeMidiGenerator(musical_tree_node=self.mt).set_musical_tree_midis()
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

class TestRelativeFractalMusicalTreeInit(TestCase):
    def test_init(self):
        FractalRelativeMusicTree(
            duration=TimelineDuration(10),
            proportions=(1, 2, 3, 4),
            main_permutation_order=(3, 1, 4, 2),
            permutation_index=(1, 1)
        )

class TestRelativeFractalMusicalTree(XMLTestCase):
    def setUp(self):
        self.ft = create_test_fractal_relative_musical_tree()
        self.ft.get_chord_factory().show_metronome = True

    def test_default_direction_iterator(self):
        for node in self.ft.traverse():
            self.assertEqual(
                node.get_chord_factory().direction_iterator.get_main_directions(), [1, -1, 1, -1]
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
                key=lambda node: node.get_chord_factory().direction_iterator.get_directions()
            ),
            expected,
        )

    def test_relative_fractal_musical_tree(self):
        self.ft.get_chord_factory().midi_value_range = (60, 84)
        RelativeTreeMidiGenerator(musical_tree_node=self.ft).set_musical_tree_midis()
        score = self.ft.export_score()
        score.staff_layout = StaffLayout()
        score.staff_layout.staff_distance = 100
        score.get_quantized = True
        with self.file_path(path, "fractal_relative") as xml_path:
            score.export_xml(xml_path)

    def test_relative_fractat_musical_ziczac_tree(self):
        for node in self.ft.traverse():
            node.get_chord_factory().direction_iterator = cycle([-1, 1])
        self.ft.get_chord_factory().midi_value_range = (60, 84)
        RelativeTreeMidiGenerator(musical_tree_node=self.ft).set_musical_tree_midis()

        score = self.ft.export_score()
        score.staff_layout = StaffLayout()
        score.staff_layout.staff_distance = 100

        score.get_quantized = True
        with self.file_path(path, "fractal_relative_ziczac") as xml_path:
            score.export_xml(xml_path)

