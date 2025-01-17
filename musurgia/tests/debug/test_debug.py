from unittest import TestCase

from musicscore.metronome import Metronome

from musurgia.trees.musicaltree import (
    FractalRelativeMusicTree,
    RelativeTreeMidiGenerator,
)
from musurgia.trees.timelinetree import TimelineDuration


class FractalRelativeMusicTreeTestCase(TestCase):
    def setUp(self):
        duration = TimelineDuration(minutes=3)
        duration.metronome = Metronome(80)
        main_permutation_order = [3, 1, 4, 5, 2]

        tgf = FractalRelativeMusicTree(
            proportions=[1, 2, 3, 4, 5],
            main_permutation_order=tuple(main_permutation_order),
            permutation_index=(1, 1),
            duration=duration,
        )
        tgf.add_layer()
        tgf.get_children()[0].get_chord_factory().show_metronome = True
        self.tgf = tgf

    def test_directions_root(self):
        self.tgf.add_layer()
        self.tgf.get_chord_factory().direction_iterator.main_direction_cell = [1, 1]
        self.tgf.get_chord_factory().midi_value_range = (60, 84)
        RelativeTreeMidiGenerator(musical_tree_node=self.tgf).set_musical_tree_midis()
        expected = """└── 72
    ├── 60.0
    │   ├── 60.0
    │   ├── 62.0
    │   ├── 63.0
    │   ├── 64.0
    │   └── 64.0
    ├── 65.0
    │   ├── 65.0
    │   ├── 65.0
    │   ├── 65.0
    │   ├── 66.0
    │   └── 66.0
    ├── 66.0
    │   ├── 66.0
    │   ├── 67.0
    │   ├── 69.0
    │   ├── 70.0
    │   └── 71.0
    ├── 73.0
    │   ├── 73.0
    │   ├── 74.0
    │   ├── 75.0
    │   ├── 76.0
    │   └── 78.0
    └── 81.0
        ├── 81.0
        ├── 82.0
        ├── 82.0
        ├── 83.0
        └── 84.0
"""
        self.assertEqual(
            self.tgf.get_tree_representation(
                key=lambda node: node.get_chord_factory().midis[0].value
            ),
            expected,
        )

    def test_directions_child(self):
        # quantize_layer(section_1.get_layer(2))

        child = self.tgf.get_children()[0]
        child.add_layer()
        child.get_chord_factory().midi_value_range = (62, 79)
        child.get_chord_factory().direction_iterator.main_direction_cell = [1, 1]
        RelativeTreeMidiGenerator(musical_tree_node=child).set_musical_tree_midis()

        print(
            [node.get_chord_factory().midis[0].value for node in child.iterate_leaves()]
        )
        # print(self.tgf.get_tree_representation(key=lambda node: node.get_chord_factory().midis[0].value))
