from pathlib import Path
from unittest import TestCase

from musicscore.score import Score

from musurgia.tests.utils_for_tests import XMLTestCase, create_test_valued_tree
from musurgia.trees.timelinetree import (
    SimpleTimelineChordFactory,
    TimelineDuration,
    TimelineTree,
)
from musicscore.chord import Chord
from musicscore.metronome import Metronome


class TimelineChordTreeTestCase(TestCase):
    def setUp(self):
        self.tlt = TimelineTree(duration=TimelineDuration(4))
        self.chf = SimpleTimelineChordFactory(self.tlt, show_metronome=True)

    def test_tree_chord(self):
        ch = self.chf.create_chord()
        self.assertTrue(isinstance(ch, Chord))
        with self.assertRaises(AttributeError):
            self.chf.chord = Chord(60, 2)
        self.assertEqual(ch.metronome.per_minute, 60)
        self.assertEqual(ch.quarter_duration, self.tlt.get_value())
        self.assertEqual(ch.midis[0].value, 72)

    def test_update_quarter_duration(self):
        self.assertEqual(self.tlt.get_duration().get_quarter_duration(), 4)
        self.tlt.get_duration().metronome = Metronome(120)
        self.assertEqual(self.chf.create_chord().quarter_duration, 8)
        self.tlt.update_duration(5)
        self.assertEqual(self.chf.create_chord().quarter_duration, 10)
        self.tlt.get_duration().metronome = Metronome(120, 2)
        self.tlt.metronome = Metronome(120, 2)
        self.assertEqual(self.chf.create_chord().quarter_duration, 20)


path = Path(__file__)


class TimeLineTreeToScoreTestCase(XMLTestCase):
    def setUp(self):
        self.vt = create_test_valued_tree()
        self.tmt = TimelineTree.create_tree_from_list(
            tree_list_representation=self.vt.get_list_representation(
                key=lambda node: node.get_value()
            ),
            represented_attribute_names="duration",
        )
        self.score = Score()

    def test_timeline_tree_layers_to_score(self):
        _show_metronome = True
        for layer_number in range(self.tmt.get_number_of_layers() + 1):
            part = self.score.add_part(f"part-{layer_number + 1}")
            layer = self.tmt.get_layer(level=layer_number)
            for node in layer:
                part.add_chord(
                    SimpleTimelineChordFactory(
                        node, show_metronome=_show_metronome
                    ).create_chord()
                )
                _show_metronome = False
        self.score.set_possible_subdivisions([2, 3, 4, 5, 6, 7, 8])
        self.score.get_quantized = True
        self.score.finalize()
        with self.file_path(path, "valued_layers_to_score") as xml_path:
            self.score.export_xml(xml_path)
