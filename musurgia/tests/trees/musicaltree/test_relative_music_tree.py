from itertools import cycle
from pathlib import Path
import timeit
from unittest import TestCase
from musicscore.layout import StaffLayout
from musurgia.musurgia_exceptions import (
    RelativeTreeChordFactoryHasNoMidiValueRangeError,
)
from musurgia.tests.utils_for_tests import (
    XMLTestCase,
    create_test_fractal_relative_musical_tree,
    test_fractal_structur_list,
)

from musurgia.trees.fractaltimelinetree import FractalTimelineTree
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
        rvg = RelativeValueGenerator(
            value_range=(60, 72), directions=[1, 1, 1, 1], proportions=[1, 2, 3, 4]
        )
        intervals = xToD(rvg)
        self.assertEqual([inter / intervals[0] for inter in intervals], [1, 2, 3, 4])
        self.assertEqual(
            [round(float(d), 2) for d in list(rvg)], [60.0, 61.2, 63.6, 67.2, 72.0]
        )


class RelativeMusicalTreeTestCase(XMLTestCase):
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


class FractalRelativeMusicalTreeTestCase(XMLTestCase):
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

    def test_relative_fractal_musical_tree_midis(self):
        self.ft.get_chord_factory().midi_value_range = (60, 84)
        RelativeTreeMidiGenerator(musical_tree_node=self.ft).set_musical_tree_midis()
        expected = """└── 72
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
                lambda node: node.get_chord_factory().midis[0].value
            ),
            expected,
        )

    def test_relative_fractal_musical_tree_midis_include_last(self):
        self.ft.get_chord_factory().midi_value_range = (60, 108)
        self.ft.get_chord_factory().direction_iterator.main_direction_cell = [1, 1]
        RelativeTreeMidiGenerator(musical_tree_node=self.ft).set_musical_tree_midis()
        selected_node = self.ft.get_children()[2].get_children()[-1]
        self.assertEqual(
            selected_node.get_chord_factory().midi_value_range, (90.0, 98.0)
        )
        self.assertEqual(
            [
                node.get_chord_factory().midi_value_range
                for node in selected_node.get_children()
            ],
            [(90.0, 91.0), (91.0, 92.0), (92.0, 95.0), (95.0, 98.0)],
        )

        ft = create_test_fractal_relative_musical_tree()
        ft.get_chord_factory().midi_value_range = (60, 108)
        ft.get_chord_factory().direction_iterator.main_direction_cell = [1, 1]

        selected_node = ft.get_children()[2].get_children()[-1]
        selected_node.get_chord_factory().include_last_midi_in_range = True
        RelativeTreeMidiGenerator(musical_tree_node=ft).set_musical_tree_midis()
        self.assertEqual(
            selected_node.get_chord_factory().midi_value_range, (90.0, 98.0)
        )
        self.assertEqual(
            [
                node.get_chord_factory().midi_value_range
                for node in selected_node.get_children()
            ],
            [(90.0, 91.0), (91.0, 94.0), (94.0, 98.0), (98.0, 98.0)],
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
        self.assertEqual(
            self.ft.get_tree_representation(
                key=lambda node: node.get_chord_factory().midis[0].value
            ),
            expected,
        )

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
        self.assertEqual(
            ft.get_tree_representation(
                key=lambda node: node.get_chord_factory().midis[0].value
            ),
            expected,
        )
        ft = _create_frmt()
        ft.get_children()[
            -2
        ].get_chord_factory().direction_iterator.main_direction_cell = [1, 1]
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
        self.assertEqual(
            ft.get_tree_representation(
                key=lambda node: node.get_chord_factory().midis[0].value
            ),
            expected,
        )

    def test_change_midi_range_of_one_child(self):
        self.ft.get_chord_factory().midi_value_range = (60, 84)
        self.ft.get_children()[0].get_chord_factory().midi_value_range = (50, 60)
        self.assertEqual(
            self.ft.get_children()[0].get_chord_factory().midi_value_range, (50, 60)
        )
        RelativeTreeMidiGenerator(musical_tree_node=self.ft).set_musical_tree_midis()
        self.assertEqual(
            self.ft.get_children()[0].get_chord_factory().midi_value_range, (50, 60)
        )
        # print(self.ft.get_tree_representation(key=lambda node: node.get_chord_factory().midis[0].value))

    def test_midi_range_exception(self):
        with self.assertRaises(RelativeTreeChordFactoryHasNoMidiValueRangeError):
            RelativeTreeMidiGenerator(
                musical_tree_node=self.ft
            ).set_musical_tree_midis()
        for child in self.ft.get_children()[1:]:
            child.get_chord_factory().midi_value_range = (60, 68)
        with self.assertRaises(RelativeTreeChordFactoryHasNoMidiValueRangeError):
            RelativeTreeMidiGenerator(
                musical_tree_node=self.ft
            ).set_musical_tree_midis()
        self.ft.get_children()[0].get_chord_factory().midi_value_range = (60, 68)
        RelativeTreeMidiGenerator(musical_tree_node=self.ft).set_musical_tree_midis()

        expected = """└── (0, 0)
    ├── (60, 68)
    │   ├── (68.0, 65.0)
    │   ├── (65.0, 60.0)
    │   │   ├── (60.0, 62.0)
    │   │   ├── (62.0, 65.0)
    │   │   ├── (65.0, 64.0)
    │   │   └── (64.0, 62.0)
    │   ├── (60.0, 61.0)
    │   └── (61.0, 65.0)
    │       ├── (62.0, 64.0)
    │       ├── (64.0, 65.0)
    │       ├── (65.0, 62.0)
    │       └── (62.0, 61.0)
    ├── (60, 68)
    ├── (60, 68)
    │   ├── (64.0, 66.0)
    │   ├── (66.0, 62.0)
    │   ├── (62.0, 68.0)
    │   │   ├── (68.0, 66.0)
    │   │   ├── (66.0, 62.0)
    │   │   ├── (62.0, 63.0)
    │   │   └── (63.0, 66.0)
    │   └── (68.0, 60.0)
    │       ├── (64.0, 62.0)
    │       ├── (62.0, 66.0)
    │       ├── (66.0, 60.0)
    │       └── (60.0, 68.0)
    └── (60, 68)
        ├── (68.0, 60.0)
        │   ├── (60.0, 63.0)
        │   ├── (63.0, 68.0)
        │   ├── (68.0, 67.0)
        │   └── (67.0, 63.0)
        ├── (60.0, 66.0)
        │   ├── (62.0, 65.0)
        │   ├── (65.0, 66.0)
        │   ├── (66.0, 62.0)
        │   └── (62.0, 60.0)
        ├── (66.0, 62.0)
        └── (62.0, 64.0)
"""
        self.assertEqual(
            self.ft.get_tree_representation(
                key=lambda node: node.get_chord_factory().midi_value_range
            ),
            expected,
        )


class FractalTimelineTreeSplitTiming(TestCase):
    def setUp(self):
        self.ft = FractalTimelineTree(
            duration=TimelineDuration(10),
            proportions=(1, 2, 3, 4),
            main_permutation_order=(3, 1, 4, 2),
            permutation_index=(1, 1),
        )

    def test_split_timing(self):
        for _ in range(5):
            self.ft.add_layer()
        leaves = list(self.ft.iterate_leaves())

        def split_me():
            leaves[0].split(1, 1, 1, 1, 1)

        execution_time = timeit.timeit(split_me, number=1)
        self.assertLess(execution_time, 1)


class FractalRelativeMusicTreeSplitTestCase(XMLTestCase):
    def setUp(self):
        self.ft = FractalRelativeMusicTree(
            duration=TimelineDuration(10),
            proportions=(1, 2, 3, 4),
            main_permutation_order=(3, 1, 4, 2),
            permutation_index=(1, 1),
        )

    def test_split_timing_without_midi(self):
        for _ in range(5):
            self.ft.add_layer()
        leaves = list(self.ft.iterate_leaves())

        def split_me():
            leaves[0].split(1, 1, 1, 1, 1)

        execution_time = timeit.timeit(split_me, number=1)
        self.assertLess(execution_time, 1)

    def test_split_timing(self):
        for _ in range(5):
            self.ft.add_layer()
        self.ft.get_chord_factory().midi_value_range = (60, 84)
        RelativeTreeMidiGenerator(musical_tree_node=self.ft).set_musical_tree_midis()
        leaves = list(self.ft.iterate_leaves())

        def split_me():
            leaves[0].split(1, 1, 1, 1, 1)

        execution_time = timeit.timeit(split_me, number=1)
        self.assertLess(execution_time, 1)

    def test_split_before_setting_midis_without_range(self):
        self.ft.split(1, 1, 1, 1, 1)
        expected = """└── None
    ├── None
    ├── None
    ├── None
    ├── None
    └── None
"""
        print(
            self.ft.get_tree_representation(
                key=lambda node: node.get_chord_factory().midi_value_range
            )
        )
        self.assertEqual(
            self.ft.get_tree_representation(
                key=lambda node: node.get_chord_factory().midi_value_range
            ),
            expected,
        )

        self.ft.get_chord_factory().midi_value_range = (60, 84)
        expected = """└── (60, 84)
    ├── None
    ├── None
    ├── None
    ├── None
    └── None
"""
        self.assertEqual(
            self.ft.get_tree_representation(
                key=lambda node: node.get_chord_factory().midi_value_range
            ),
            expected,
        )

        RelativeTreeMidiGenerator(musical_tree_node=self.ft).set_musical_tree_midis()
        expected = """└── (60, 84)
    ├── (84.0, 79.0)
    ├── (79.0, 74.0)
    ├── (74.0, 70.0)
    ├── (70.0, 65.0)
    └── (65.0, 60.0)
"""
        self.assertEqual(
            self.ft.get_tree_representation(
                key=lambda node: node.get_chord_factory().midi_value_range
            ),
            expected,
        )

    def test_split_before_setting_midis_with_range(self):
        self.ft.get_chord_factory().midi_value_range = (60, 84)
        self.ft.split(1, 1, 1, 1, 1)
        expected = """└── (60, 84)
    ├── (60, 84)
    ├── (60, 84)
    ├── (60, 84)
    ├── (60, 84)
    └── (60, 84)
"""
        self.assertEqual(
            self.ft.get_tree_representation(
                key=lambda node: node.get_chord_factory().midi_value_range
            ),
            expected,
        )

        RelativeTreeMidiGenerator(musical_tree_node=self.ft).set_musical_tree_midis()
        self.assertEqual(
            self.ft.get_tree_representation(
                key=lambda node: node.get_chord_factory().midi_value_range
            ),
            expected,
        )

    def test_split_after_setting_midis(self):
        self.ft.get_chord_factory().midi_value_range = (60, 84)
        RelativeTreeMidiGenerator(musical_tree_node=self.ft).set_musical_tree_midis()
        self.ft.split(1, 1, 1, 1, 1)
        expected = """└── (60, 84)
    ├── (60, 84)
    ├── (60, 84)
    ├── (60, 84)
    ├── (60, 84)
    └── (60, 84)
"""
        self.assertEqual(
            self.ft.get_tree_representation(
                key=lambda node: node.get_chord_factory().midi_value_range
            ),
            expected,
        )
