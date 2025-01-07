from itertools import cycle
from pathlib import Path
from unittest import TestCase

from musicscore import midi
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
    RelativeMusicTree,
    RelativeTreeChordFactory,
    RelativeTreeMidiGenerator,
)
from musurgia.trees.timelinetree import TimelineDuration
from musurgia.utils import RelativeValueGenerator, xToD

path = Path(__file__)

class RelativeValueGeneratorTestCase(TestCase):
    def test_rfg_with_1_1(self):
        rvg = RelativeValueGenerator(value_range=(60, 72), directions=[1, 1, 1, 1], proportions=[1, 2, 3, 4])
        intervals = xToD(rvg)
        self.assertEqual([inter /  intervals[0] for inter in intervals], [1, 2, 3, 4])
        self.assertEqual([round(float(d), 2) for d in list(rvg)], [60.0, 61.2, 63.6, 67.2, 72.0])

class TestRelativeMusicalTree(XMLTestCase):
    def setUp(self):
        self.mt = RelativeMusicTree.create_tree_from_list(
            test_fractal_structur_list, "duration"
        )
        self.mt.get_chord_factory().show_metronome = True
        self.mt.get_chord_factory().midi_value_range = (60, 84)

    def test_chord_factory(self):
        self.assertTrue(self.mt.get_chord_factory(), RelativeTreeChordFactory)
        rtm = RelativeTreeMidiGenerator(musical_tree_node=self.mt)
        self.assertEqual(rtm.get_musical_tree_node(), self.mt)
        self.assertTrue(
            rtm.get_musical_tree_node().get_chord_factory(), RelativeTreeChordFactory
        )

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
            permutation_index=(1, 1),
        )


class TestRelativeFractalMusicalTree(XMLTestCase):
    def setUp(self):
        self.ft = create_test_fractal_relative_musical_tree()
        self.ft.get_chord_factory().show_metronome = True

    def test_default_direction_iterator(self):
        for node in self.ft.traverse():
            self.assertEqual(
                node.get_chord_factory().direction_iterator.get_main_directions(),
                [1, -1, 1, -1],
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

    def test_main_direction_cell(self):
        for node in self.ft.traverse():
            self.assertEqual(
                node.get_chord_factory().direction_iterator.main_direction_cell, [1, -1]
            )

        self.ft.get_chord_factory().direction_iterator.main_direction_cell = [-1, 1]

        for node in self.ft.traverse():
            self.assertEqual(
                node.get_chord_factory().direction_iterator.main_direction_cell, [-1, 1]
            )

    def test_same_direction_cells(self):
        self.ft.get_chord_factory().direction_iterator.main_direction_cell = [1, 1]
        self.ft.get_chord_factory().midi_value_range = (60, 84)
        RelativeTreeMidiGenerator(musical_tree_node=self.ft).set_musical_tree_midis()
        expected = """└── 72
    ├── 60.0
    │   ├── 60.0
    │   ├── 61.0
    │   │   ├── 61.0
    │   │   ├── 62.0
    │   │   ├── 63.0
    │   │   └── 63.0
    │   ├── 64.0
    │   └── 65.0
    │       ├── 65.0
    │       ├── 66.0
    │       ├── 66.0
    │       └── 67.0
    ├── 67.0
    ├── 70.0
    │   ├── 70.0
    │   ├── 71.0
    │   ├── 73.0
    │   │   ├── 73.0
    │   │   ├── 73.0
    │   │   ├── 74.0
    │   │   └── 74.0
    │   └── 75.0
    │       ├── 75.0
    │       ├── 75.0
    │       ├── 76.0
    │       └── 77.0
    └── 79.0
        ├── 79.0
        │   ├── 79.0
        │   ├── 79.0
        │   ├── 80.0
        │   └── 80.0
        ├── 81.0
        │   ├── 81.0
        │   ├── 81.0
        │   ├── 81.0
        │   └── 82.0
        ├── 82.0
        └── 83.0
"""
        self.assertEqual(self.ft.get_tree_representation(key=lambda node: node.get_chord_factory().midis[0].value), expected)

    def test_change_directions_of_one_child(self):
        def _create_frmt():
            ft = FractalRelativeMusicTree(
            duration=TimelineDuration(10),
            proportions=(1, 2, 3, 4),
            main_permutation_order=(3, 1, 4, 2),
            permutation_index=(1, 1),
            )
            ft.add_layer()
            ft.add_layer()
            ft.add_layer()
            ft.get_chord_factory().midi_value_range = (60, 84)
            return ft
        ft = _create_frmt()
        RelativeTreeMidiGenerator(musical_tree_node=ft).set_musical_tree_midis()
        expected = """└── 72
    ├── 68.0
    │   ├── 80.0
    │   │   ├── 78.0
    │   │   ├── 77.0
    │   │   ├── 79.0
    │   │   └── 76.0
    │   ├── 76.0
    │   │   ├── 68.0
    │   │   ├── 71.0
    │   │   ├── 76.0
    │   │   └── 75.0
    │   ├── 68.0
    │   │   ├── 70.0
    │   │   ├── 68.0
    │   │   ├── 69.0
    │   │   └── 68.0
    │   └── 70.0
    │       ├── 72.0
    │       ├── 75.0
    │       ├── 76.0
    │       └── 72.0
    ├── 80.0
    │   ├── 81.0
    │   │   ├── 83.0
    │   │   ├── 81.0
    │   │   ├── 82.0
    │   │   └── 81.0
    │   ├── 83.0
    │   │   ├── 83.0
    │   │   ├── 84.0
    │   │   ├── 83.0
    │   │   └── 84.0
    │   ├── 84.0
    │   │   ├── 83.0
    │   │   ├── 81.0
    │   │   ├── 81.0
    │   │   └── 83.0
    │   └── 81.0
    │       ├── 80.0
    │       ├── 80.0
    │       ├── 81.0
    │       └── 81.0
    ├── 84.0
    │   ├── 76.0
    │   │   ├── 75.0
    │   │   ├── 73.0
    │   │   ├── 72.0
    │   │   └── 75.0
    │   ├── 72.0
    │   │   ├── 80.0
    │   │   ├── 72.0
    │   │   ├── 78.0
    │   │   └── 74.0
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
        │   ├── 64.0
        │   ├── 65.0
        │   ├── 63.0
        │   └── 66.0
        └── 66.0
            ├── 64.0
            ├── 66.0
            ├── 64.0
            └── 65.0
"""
        self.assertEqual(ft.get_tree_representation(key=lambda node: node.get_chord_factory().midis[0].value), expected)
        ft = _create_frmt()
        ft.get_children()[-2].get_chord_factory().direction_iterator.main_direction_cell = [1, 1]
        RelativeTreeMidiGenerator(musical_tree_node=ft).set_musical_tree_midis()
        expected = """└── 72
    ├── 68.0
    │   ├── 80.0
    │   │   ├── 78.0
    │   │   ├── 77.0
    │   │   ├── 79.0
    │   │   └── 76.0
    │   ├── 76.0
    │   │   ├── 68.0
    │   │   ├── 71.0
    │   │   ├── 76.0
    │   │   └── 75.0
    │   ├── 68.0
    │   │   ├── 70.0
    │   │   ├── 68.0
    │   │   ├── 69.0
    │   │   └── 68.0
    │   └── 70.0
    │       ├── 72.0
    │       ├── 75.0
    │       ├── 76.0
    │       └── 72.0
    ├── 80.0
    │   ├── 81.0
    │   │   ├── 83.0
    │   │   ├── 81.0
    │   │   ├── 82.0
    │   │   └── 81.0
    │   ├── 83.0
    │   │   ├── 83.0
    │   │   ├── 84.0
    │   │   ├── 83.0
    │   │   └── 84.0
    │   ├── 84.0
    │   │   ├── 83.0
    │   │   ├── 81.0
    │   │   ├── 81.0
    │   │   └── 83.0
    │   └── 81.0
    │       ├── 80.0
    │       ├── 80.0
    │       ├── 81.0
    │       └── 81.0
    ├── 84.0
    │   ├── 84.0
    │   │   ├── 84.0
    │   │   ├── 83.0
    │   │   ├── 83.0
    │   │   └── 82.0
    │   ├── 82.0
    │   │   ├── 82.0
    │   │   ├── 81.0
    │   │   ├── 80.0
    │   │   └── 79.0
    │   ├── 79.0
    │   │   ├── 79.0
    │   │   ├── 78.0
    │   │   ├── 76.0
    │   │   └── 75.0
    │   └── 74.0
    │       ├── 74.0
    │       ├── 73.0
    │       ├── 72.0
    │       └── 70.0
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
        │   ├── 64.0
        │   ├── 65.0
        │   ├── 63.0
        │   └── 66.0
        └── 66.0
            ├── 64.0
            ├── 66.0
            ├── 64.0
            └── 65.0
"""
        self.assertEqual(ft.get_tree_representation(key=lambda node: node.get_chord_factory().midis[0].value), expected)