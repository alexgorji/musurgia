import os
from itertools import cycle

from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.agrandom import AGRandom
from musurgia.agunittest import AGTestCase
from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.chordfield.chordfield import ChordFieldGroup, ChordField

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        cf_1 = ChordField(quarter_duration=3, midi_generator=cycle([60, 61, 64, 66]))
        cf_2 = ChordField(quarter_duration=6, midi_generator=cycle([72, 73, 74, 73, 72]))
        cfg = ChordFieldGroup()
        cfg.add_field(cf_1)
        cfg.add_field(cf_2)
        xml_path = path + 'test_1.xml'
        cfg.simple_format.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        cf_1 = ChordField(quarter_duration=3, midi_generator=cycle([60, 61, 64, 66]))
        cf_2 = ChordField(quarter_duration=6, midi_generator=cycle([72, 73, 74, 73, 72]))
        cfg = ChordFieldGroup(duration_generator=AGRandom(pool=[0.2, 0.4, 0.8, 1.6], seed=10))
        cfg.add_field(cf_1)
        cfg.add_field(cf_2)
        xml_path = path + 'test_2.xml'
        cfg.simple_format.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_3(self):
        cf_1 = ChordField(quarter_duration=3, midi_generator=cycle([60, 61, 64, 66]), duration_generator=cycle([1]))
        cf_2 = ChordField(quarter_duration=6, midi_generator=cycle([72, 73, 74, 73, 72]))
        cfg = ChordFieldGroup(duration_generator=AGRandom(pool=[0.2, 0.4, 0.8, 1.6], seed=10))
        cfg.add_field(cf_1)
        cfg.add_field(cf_2)
        xml_path = path + 'test_3.xml'
        cfg.simple_format.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_4(self):
        cf_1 = ChordField(quarter_duration=3, midi_generator=cycle([60, 61, 64, 66]))
        cf_2 = ChordField(quarter_duration=6, midi_generator=cycle([72, 73, 74, 73, 72]))
        cfg = ChordFieldGroup(duration_generator=ArithmeticProgression(a1=0.3, an=1.5))
        cfg.add_field(cf_1)
        cfg.add_field(cf_2)
        xml_path = path + 'test_4.xml'
        cfg.simple_format.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
