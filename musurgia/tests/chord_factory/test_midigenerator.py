from unittest import TestCase

from musicscore.midi import Midi

from musurgia.chordfactory.midigenerators import (
    RandomMidiGenerator,
    RelativeMidiGenerator,
)


class RandomMidiGeneratorTestCase(TestCase):
    def setUp(self):
        self.rmg = RandomMidiGenerator(
            pool=[60, 61, 62.5, 64, 52], periodicity=2, seed=10
        )

    def test_generate_random_midis(self):
        random_midis = [next(self.rmg) for _ in range(10)]
        for midi in random_midis:
            self.assertTrue(isinstance(midi, Midi))
        self.assertListEqual(
            [m.value for m in random_midis], [52, 60, 64, 52, 60, 61, 64, 62.5, 61, 60]
        )


class RelativeMidiGeneratorTestCase(TestCase):
    def setUp(self):
        self.remg = RelativeMidiGenerator(
            value_range=[44, 54], proportions=[2, 4, 1, 3], directions=[-1, -1, 1, 1]
        )

    def test_init_relative_midi_generator(self):
        expected = [54.0, 51.0, 44.0, 46.0, 51.0]
        self.assertListEqual([midi.value for midi in self.remg], expected)
