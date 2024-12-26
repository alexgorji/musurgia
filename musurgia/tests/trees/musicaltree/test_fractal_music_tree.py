from pathlib import Path

from musicscore.score import Score
from musurgia.tests.utils_for_tests import XMLTestCase, create_test_fractal_musical_tree

path = Path(__file__)


class TestSimpleFractalMusicalTree(XMLTestCase):
    def setUp(self):
        self.ft = create_test_fractal_musical_tree()

    def test_midi_values(self):
        expected = """└── [72]
    ├── [72]
    │   ├── [72]
    │   ├── [72]
    │   │   ├── [72]
    │   │   ├── [72]
    │   │   ├── [72]
    │   │   └── [72]
    │   ├── [72]
    │   └── [72]
    │       ├── [72]
    │       ├── [72]
    │       ├── [72]
    │       └── [72]
    ├── [72]
    ├── [72]
    │   ├── [72]
    │   ├── [72]
    │   ├── [72]
    │   │   ├── [72]
    │   │   ├── [72]
    │   │   ├── [72]
    │   │   └── [72]
    │   └── [72]
    │       ├── [72]
    │       ├── [72]
    │       ├── [72]
    │       └── [72]
    └── [72]
        ├── [72]
        │   ├── [72]
        │   ├── [72]
        │   ├── [72]
        │   └── [72]
        ├── [72]
        │   ├── [72]
        │   ├── [72]
        │   ├── [72]
        │   └── [72]
        ├── [72]
        └── [72]
"""
        self.assertEqual(
            self.ft.get_tree_representation(
                key=lambda node: [midi.value for midi in node.get_chord_factory().midis]
            ),
            expected,
        )

    def test_create_chord(self):
        count = 0
        for node in self.ft.traverse():
            count += 1
            chord = node.get_chord_factory().create_chord()
            self.assertEqual(
                chord.quarter_duration, node.get_duration().get_quarter_duration()
            )

        self.assertEqual(count, 41)

    def test_simple_fractal_musical_tree_first_layer(self):
        score = Score()
        part = score.add_part("part-1")
        for node in self.ft.get_layer(1):
            part.add_chord(node.get_chord_factory().create_chord())

        with self.file_path(path, "simple_first_layer") as xml_path:
            score.export_xml(xml_path)

    def test_simple_fractal_musical_tree(self):
        score = self.ft.export_score()
        score.get_quantized = True
        with self.file_path(path, "simple") as xml_path:
            score.export_xml(xml_path)
