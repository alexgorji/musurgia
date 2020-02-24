import os
from itertools import cycle

from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.agrandom import AGRandom
from musurgia.agunittest import AGTestCase
from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.chordfield.chordfield import ChordFieldGroup, ChordField, Breathe
from musurgia.interpolation import InterpolationGroup, RandomInterpolation, Interpolation

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
        cf_1 = ChordField(quarter_duration=3, midi_generator=cycle([60, 61, 64, 66]), long_ending_mode='post')
        cf_2 = ChordField(quarter_duration=6, midi_generator=cycle([72, 73, 74, 73, 72]))
        cfg = ChordFieldGroup(duration_generator=ArithmeticProgression(a1=0.3, an=1.5))
        cfg.add_field(cf_1)
        cfg.add_field(cf_2)
        xml_path = path + 'test_4.xml'
        cfg.simple_format.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_5(self):
        cf_1 = ChordField(quarter_duration=7, midi_generator=cycle([60, 61, 64, 66]), long_ending_mode=None)
        cf_2 = ChordField(quarter_duration=8, midi_generator=cycle([72, 73, 74, 73, 72]))
        duration_generator = InterpolationGroup()
        duration_generator.add_section(2, 2, 3)
        duration_generator.add_section(2, 0.2, 3)
        duration_generator.add_section(0.2, 0.2, 3)
        duration_generator.add_section(0.2, 2, 3)
        duration_generator.add_section(2, 2, 3)
        cfg = ChordFieldGroup(duration_generator=duration_generator)
        cfg.add_field(cf_1)
        cfg.add_field(cf_2)
        xml_path = path + 'test_5.xml'
        cfg.simple_format.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_6(self):
        br = Breathe(quarter_durations=[3, 5, 3, 5, 6])
        br.repose_1.duration_generator = RandomInterpolation(start=[1, 1.2, 1.4], end=[1, 1.2, 1.4], seed=10)
        br.inspiration.duration_generator = RandomInterpolation(start=[1, 1.2, 1.4], end=[0.2, 0.2, 0.4], seed=11)
        br.climax.duration_generator = RandomInterpolation(start=[0.2, 0.2, 0.4], end=[0.2, 0.2, 0.4], seed=12)
        br.expiration.duration_generator = RandomInterpolation(start=[0.2, 0.2, 0.4], end=[1, 1.2, 1.4], seed=13)
        br.repose_2.duration_generator = RandomInterpolation(start=[1, 1.2, 1.4], end=[1, 1.2, 1.4], seed=14)

        xml_path = path + 'test_6.xml'
        br.simple_format.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_7(self):
        cf_1 = ChordField(quarter_duration=7, midi_generator=cycle([60, 61, 64, 66]), long_ending_mode='post')
        cf_2 = ChordField(quarter_duration=8, midi_generator=cycle([72, 73, 74, 73, 72]), long_ending_mode=None)
        duration_generator = InterpolationGroup()
        duration_generator.add_interpolation(
            RandomInterpolation(start=[1, 1.2, 1.4], end=[1, 1.2, 1.4], seed=10, duration=3)
        )
        duration_generator.add_interpolation(
            RandomInterpolation(start=[1, 1.2, 1.4], end=[0.2, 0.2, 0.4], seed=11, duration=5)
        )
        duration_generator.add_interpolation(
            RandomInterpolation(start=[0.2, 0.2, 0.4], end=[0.2, 0.2, 0.4], seed=12, duration=3)
        )
        duration_generator.add_interpolation(
            RandomInterpolation(start=[0.2, 0.2, 0.4], end=[1, 1.2, 1.4], seed=13, duration=5)
        )
        duration_generator.add_interpolation(
            RandomInterpolation(start=[1, 1.2, 1.4], end=[1, 1.2, 1.4], seed=14, duration=3)
        )
        cfg = ChordFieldGroup(duration_generator=duration_generator)
        cfg.add_field(cf_1)
        cfg.add_field(cf_2)
        xml_path = path + 'test_7.xml'
        cfg.simple_format.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_8(self):
        # cf_1 = ChordField(quarter_duration=3, midi_generator=cycle([60, 61, 64, 66]), long_ending_mode=None)
        cf_2 = ChordField(quarter_duration=5, midi_generator=cycle([72, 73, 74, 73, 72]), long_ending_mode=None)
        cf_3 = ChordField(quarter_duration=3, midi_generator=cycle([60, 61, 64, 66]), long_ending_mode=None)
        cf_4 = ChordField(quarter_duration=5, midi_generator=cycle([72, 73, 74, 73, 72]), long_ending_mode='post')
        # cf_5 = ChordField(quarter_duration=3, midi_generator=cycle([60, 61, 64, 66]), long_ending_mode=None)
        # cf_1.duration_generator = cycle([1.5])
        # cf_2.duration_generator = ArithmeticProgression(a1=1.5, an=0.2)
        cf_2.duration_generator = Interpolation(start=1.5, end=0.2)
        cf_3.duration_generator = cycle([0.2])
        cf_4.duration_generator = Interpolation(start=0.2, end=1.5, mode='duration')
        # cf_5.duration_generator = cycle([1.5])
        cfg = ChordFieldGroup()
        # cfg.add_field(cf_1)
        cfg.add_field(cf_2)
        cfg.add_field(cf_3)
        cfg.add_field(cf_4)
        # cfg.add_field(cf_5)
        xml_path = path + 'test_8.xml'
        cfg.simple_format.to_stream_voice().add_to_score(self.score)
        self.score.max_division = 5
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
