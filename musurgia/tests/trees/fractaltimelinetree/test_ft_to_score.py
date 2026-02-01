from pathlib import Path
from unittest import TestCase

from musicscore.score import Score
from musurgia.tests.helpers import (
    XMLTestCase,
    create_test_fractal_timeline_tree,
)
from musurgia.trees.timelinetree import SimpleTimelineChordFactory

path = Path(__file__)


class SimpleFractalTreeChordFactory(SimpleTimelineChordFactory):
    pass


class TestSimpleFractalTreeChordFactory(TestCase):
    def setUp(self) -> None:
        self.ft = create_test_fractal_timeline_tree()

    def test_node(self):
        sftchf = SimpleFractalTreeChordFactory(timline_node=self.ft)
        assert sftchf._timeline_node == self.ft
        chord = sftchf.create_chord()
        assert (
            chord.quarter_duration.value
            == self.ft.get_duration().calculate_in_seconds()
        )


class TestFtToScore(XMLTestCase):
    def setUp(self) -> None:
        self.ft = create_test_fractal_timeline_tree()
        self.score = Score()

    def test_fractal_timeline_tree_durations(self):
        expected = """└── 10
    ├── 3
    │   ├── 3/5
    │   ├── 6/5
    │   │   ├── 6/25
    │   │   ├── 12/25
    │   │   ├── 3/25
    │   │   └── 9/25
    │   ├── 3/10
    │   └── 9/10
    │       ├── 27/100
    │       ├── 9/100
    │       ├── 9/25
    │       └── 9/50
    ├── 1
    ├── 4
    │   ├── 2/5
    │   ├── 4/5
    │   ├── 6/5
    │   │   ├── 6/25
    │   │   ├── 12/25
    │   │   ├── 3/25
    │   │   └── 9/25
    │   └── 8/5
    │       ├── 4/25
    │       ├── 8/25
    │       ├── 12/25
    │       └── 16/25
    └── 2
        ├── 4/5
        │   ├── 4/25
        │   ├── 8/25
        │   ├── 2/25
        │   └── 6/25
        ├── 3/5
        │   ├── 9/50
        │   ├── 3/50
        │   ├── 6/25
        │   └── 3/25
        ├── 2/5
        └── 1/5
"""
        self.assertEqual(
            self.ft.get_tree_representation(
                key=lambda node: node.get_duration().calculate_in_seconds()
            ),
            expected,
        )
        expected = """└── QuarterDuration: 10
    ├── QuarterDuration: 3
    │   ├── QuarterDuration: 3/5
    │   ├── QuarterDuration: 6/5
    │   │   ├── QuarterDuration: 6/25
    │   │   ├── QuarterDuration: 12/25
    │   │   ├── QuarterDuration: 3/25
    │   │   └── QuarterDuration: 9/25
    │   ├── QuarterDuration: 3/10
    │   └── QuarterDuration: 9/10
    │       ├── QuarterDuration: 27/100
    │       ├── QuarterDuration: 9/100
    │       ├── QuarterDuration: 9/25
    │       └── QuarterDuration: 9/50
    ├── QuarterDuration: 1
    ├── QuarterDuration: 4
    │   ├── QuarterDuration: 2/5
    │   ├── QuarterDuration: 4/5
    │   ├── QuarterDuration: 6/5
    │   │   ├── QuarterDuration: 6/25
    │   │   ├── QuarterDuration: 12/25
    │   │   ├── QuarterDuration: 3/25
    │   │   └── QuarterDuration: 9/25
    │   └── QuarterDuration: 8/5
    │       ├── QuarterDuration: 4/25
    │       ├── QuarterDuration: 8/25
    │       ├── QuarterDuration: 12/25
    │       └── QuarterDuration: 16/25
    └── QuarterDuration: 2
        ├── QuarterDuration: 4/5
        │   ├── QuarterDuration: 4/25
        │   ├── QuarterDuration: 8/25
        │   ├── QuarterDuration: 2/25
        │   └── QuarterDuration: 6/25
        ├── QuarterDuration: 3/5
        │   ├── QuarterDuration: 9/50
        │   ├── QuarterDuration: 3/50
        │   ├── QuarterDuration: 6/25
        │   └── QuarterDuration: 3/25
        ├── QuarterDuration: 2/5
        └── QuarterDuration: 1/5
"""
        self.assertEqual(
            self.ft.get_tree_representation(
                key=lambda node: node.get_duration().get_quarter_duration()
            ),
            expected,
        )

    def test_fractal_timeline_tree_layers_to_score_simple(self):
        _show_metronome = True
        for layer_number in range(self.ft.get_number_of_layers() + 1):
            part = self.score.add_part(f"part-{layer_number + 1}")
            layer = self.ft.get_layer(level=layer_number)
            for node in layer:
                chord = SimpleFractalTreeChordFactory(
                    node, show_metronome=_show_metronome
                ).create_chord()
                part.add_chord(chord)
                _show_metronome = False
        self.score.set_possible_subdivisions([2, 3, 4, 5, 6, 7, 8])
        self.score.get_quantized = True
        self.score.finalize()
        with self.file_path(path, "simple") as xml_path:
            self.score.export_xml(xml_path)
