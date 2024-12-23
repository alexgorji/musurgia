from unittest import TestCase

from musicscore.chord import XMLWords

from musurgia.chordfactory.chordfactory import AbstractChordFactory


class SimpleDemoChordFactory(AbstractChordFactory):
    def update_chord_quarter_duration(self):
        self._chord.quarter_duration.value = 4

    def update_chord_midis(self):
        self._chord.midis = 72

    def update_chord_words(self):
        self._chord.add_x(XMLWords("something"))


class ChordFactoryTestCase(TestCase):
    def test_simple_demo_chord_factory(self):
        chf = SimpleDemoChordFactory()
        ch = chf.create_chord()
        self.assertEqual(ch.midis[0].value, 72)
        self.assertEqual(ch.quarter_duration, 4)
        self.assertEqual(ch.get_words()[0].value_, "something")
