import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.agunittest import AGTestCase
from musurgia.chordfield.chordfield import ChordField2
from musurgia.chordfield.valuegenerator import ValueGenerator

path = str(os.path.abspath(__file__).split('.')[0])


def duration_generator(first_duration=1, delta=0.5):
    current_duration = first_duration
    while True:
        yield current_duration
        current_duration += delta


class Test(AGTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        # chord_generator with enough chords simple
        field = ChordField2(quarter_duration=10,
                            chord_generator=ValueGenerator(
                                iter(SimpleFormat(quarter_durations=[3, 2, 1, 2, 3, 4, 5]).chords)))
        self.score.set_time_signatures(quarter_durations=field.quarter_duration)
        field.simple_format.to_stream_voice().add_to_score(self.score)

        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        # chord_generator with not enough chords simple
        field = ChordField2(quarter_duration=10,
                            chord_generator=ValueGenerator(
                                iter(SimpleFormat(quarter_durations=[3, 2]).chords)))
        # self.score.set_time_signatures(quarter_durations=field.quarter_duration)
        field.simple_format.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_2.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
        #
        # def test_2(self):
        #     field = ChordField(10)
        #     field.duration_generator = ArithmeticProgression(a1=1, an=2)
        #     field.simple_format.to_stream_voice().add_to_score(self.score)
        #     xml_path = path + '_test_2.xml'
        #     self.score.write(xml_path)
        #     self.assertCompareFiles(xml_path)
        #
        # def test_3(self):
        #     field = ChordField(10)
        #     field.duration_generator = AGRandom(pool=[0.2, 0.4, 0.8, 1.2, 1.6, 2], periodicity=3, seed=20)
        #     field.simple_format.to_stream_voice().add_to_score(self.score)
        #     xml_path = path + '_test_3.xml'
        #     self.score.write(xml_path)
        #     self.assertCompareFiles(xml_path)
        #
        # def test_4(self):
        #     field = ChordField(10, long_ending_mode='post')
        #     field.duration_generator = duration_generator(first_duration=1, delta=0.2)
        #     field.simple_format.to_stream_voice().add_to_score(self.score)
        #     xml_path = path + '_test_4.xml'
        #     self.score.write(xml_path)
        #     self.assertCompareFiles(xml_path)
        #
        # def test_5(self):
        #     field = ChordField(10, long_ending_mode='post')
        #     field.duration_generator = AGRandom(pool=[0.2, 0.4, 0.8, 1.2, 1.6, 2], periodicity=3, seed=20)
        #     field.midi_generator = Interpolation(start=84, end=60, duration=None, key=lambda x: int(x))
        #     field.simple_format.to_stream_voice().add_to_score(self.score)
        #     xml_path = path + '_test_5.xml'
        #     self.score.write(xml_path)
        #     self.assertCompareFiles(xml_path)
        #
        # def test_6(self):
        #     field = ChordField(quarter_duration=10, duration_generator=ArithmeticProgression(a1=0.2, an=2),
        #                        midi_generator=Interpolation(start=84, end=60, duration=None,
        #                                                     key=lambda midi: round(midi * 2) / 2))
        #     field.short_ending_mode = 'prolong'
        #     field.simple_format.to_stream_voice().add_to_score(self.score)
        #     xml_path = path + '_test_6.xml'
        #     self.score.write(xml_path)
        #     self.assertCompareFiles(xml_path)
