from pathlib import Path
from unittest import TestCase

from musicscore import SimpleFormat, Score, Metronome, Id, Part
from quicktions import Fraction

from musurgia.random import Random


def sams_get_quantized_durations(quarter_durations, possible_subdivisions):
    dummy_chords = SimpleFormat(quarter_durations=quarter_durations).chords
    import time
    dummy_part = Part(id=f'p_{time.time_ns()}')
    dummy_part.set_possible_subdivisions(possible_subdivisions)
    dummy_part.get_quantized = True
    [dummy_part.add_chord(ch) for ch in dummy_chords]

    dummy_part.finalize()
    quantized = [dummy_part.get_chords()[0].quarter_duration]
    for ch in dummy_part.get_chords()[1:]:
        if ch.is_tied_to_previous:
            quantized[-1] += ch.quarter_duration
        else:
            quantized.append(ch.quarter_duration)
    return quantized


class TestRandomExample(TestCase):
    def setUp(self) -> None:
        Id.__refs__.clear()  # it is needed to be able to use unique part ids again!

    def test_random_example_1_proportions(self):
        """Sam wants to compose a little piece for flute solo. She starts with planing the whole duration of the
        piece. Or maybe only of a section of the piece?"""
        pool = [1, 2, 3, 4, 5]
        seed = 10
        periodicity = 3
        r = Random(pool=pool, seed=seed, periodicity=periodicity)
        proportions = [next(r) for _ in range(len(pool))]  # [5, 1, 4, 2, 3]
        """She likes the proportions: No number is at its original position. The differences are manifold: -4, +3, 
        -2, +1 [, +2]
        """
        """
        She now want to see these proportions in action. She converts theme temporarily to to musical durations
        without deciding now about the tempo. Let's say the unit is a whole note duration.
        """
        chords = SimpleFormat(quarter_durations=[x * 4 for x in proportions]).chords
        [ch.add_lyric(ch.quarter_duration) for ch in chords]
        score = Score(title='random example 1 proportions')
        part = score.add_part(id='part_1')
        [part.add_chord(ch) for ch in chords]
        path = Path(__file__)
        current_path = path.with_stem(path.stem + '_1_proportions').with_suffix('.xml')
        score.export_xml(path=current_path)
        """
        Isn't it better to have in all 5 sections the same quarter duration and different tempi? Let's try it out!
        """

    def test_random_example_2_proportions_with_tempi(self):
        ####################
        pool = [1, 2, 3, 4, 5]
        seed = 10
        periodicity = 3
        r = Random(pool=pool, seed=seed, periodicity=periodicity)
        proportions = [next(r) for _ in range(len(pool))]  # [5, 1, 4, 2, 3]
        ####################
        """
        Isn't it better to have in all 5 sections the same quarter duration and different tempi? Let's try it out!
        """
        tempo_1 = 5 * 6  # 30 the slowest tempo (5)
        tempo_2 = 5 * 5 * 6  # 150 the fastest tempo (1)
        all_tempi = [tempo_1 + (tempo_2 - tempo_1) * i / 4 for i in range(5)]  # a simple arithmetic progression
        section_quarter_duration = 5 * 4

        def generate_chords_1():
            output = SimpleFormat(quarter_durations=[section_quarter_duration for _ in range(5)]).chords
            durations = [section_quarter_duration * 60 / t for t in all_tempi]
            for i in range(5):
                ch = output[i]
                ch.add_lyric(f'{i + 1} duration = {round(durations[i], 2)}"')
                ch.metronome = Metronome(all_tempi[i])
            output = [output[p - 1] for p in proportions]
            return output

        score = Score(title='random example 2 proportions with tempi')
        part = score.add_part(id='part_1')
        [part.add_chord(ch) for ch in generate_chords_1()]
        for measure_number in [5 + i * 5 for i in range(5)]:
            part.get_measure(measure_number).set_barline(style='light-light')
        path = Path(__file__)
        current_path = path.with_stem(path.stem + '_2_proportions_with_tempi').with_suffix('.xml')
        score.export_xml(path=current_path)
        """
        Ok! Now we can go on with the time structure and divide each section in 5 with random durations.
        """

    def test_random_example_3_layer_1(self):
        ####################
        pool = [1, 2, 3, 4, 5]
        seed = 10
        periodicity = 3
        r = Random(pool=pool, seed=seed, periodicity=periodicity)
        proportions = [next(r) for _ in range(len(pool))]  # [5, 1, 4, 2, 3]
        tempo_1 = 5 * 6  # 30 the slowest tempo (5)
        tempo_2 = 5 * 5 * 6  # 150 the fastest tempo (1)
        all_tempi = [tempo_1 + (tempo_2 - tempo_1) * i / 4 for i in range(5)]  # a simple arithmetic progression
        section_quarter_duration = 5 * 4

        def generate_chords_1():
            output = SimpleFormat(quarter_durations=[section_quarter_duration for _ in range(5)]).chords
            durations = [section_quarter_duration * 60 / t for t in all_tempi]
            for i in range(5):
                ch = output[i]
                ch.add_lyric(f'{i + 1} duration = {round(durations[i], 2)}"')
                ch.metronome = Metronome(all_tempi[i])
            output = [output[p - 1] for p in proportions]
            return output

        ####################
        """
        Ok! Now we can go on with the time structure and divide each section in 5 with random durations.
        """
        layer_1_proportions = [[r.__next__() for _ in range(5)] for x in range(5)]
        # [[1, 5, 4, 3, 1], [2, 4, 5, 3, 2], [4, 5, 1, 2, 3], [5, 4, 1, 3, 5], [2, 4, 1, 3, 5]]
        layer_1_quarter_durations = [
            [(Fraction(p, sum(layer_1_proportions[i]))) * section_quarter_duration for p in layer_1_proportions[i]]
            for i in range(5)]

        # [[Fraction(10, 7), Fraction(50, 7), Fraction(40, 7), Fraction(30, 7), Fraction(10, 7)], [Fraction(5, 2),
        # Fraction(5, 1), Fraction(25, 4), Fraction(15, 4), Fraction(5, 2)], [Fraction(16, 3), Fraction(20, 3),
        # Fraction(4, 3), Fraction(8, 3), Fraction(4, 1)], [Fraction(50, 9), Fraction(40, 9), Fraction(10, 9),
        # Fraction(10, 3), Fraction(50, 9)], [Fraction(8, 3), Fraction(16, 3), Fraction(4, 3), Fraction(4, 1),
        # Fraction(20, 3)]]

        score = Score(title='random example 3 layer 1')
        part = score.add_part(id='part_1')
        [part.add_chord(ch) for ch in generate_chords_1()]

        part = score.add_part(id='part_2')
        chords_layer_1 = SimpleFormat(quarter_durations=[qd for l in layer_1_quarter_durations for qd in l]).chords

        part.set_possible_subdivisions([2])  # quantization with only eights
        part.get_quantized = True  # is needed to turn quantization on
        [part.add_chord(ch) for ch in chords_layer_1]
        for measure_number in [5 + i * 5 for i in range(5)]:
            part.get_measure(measure_number).set_barline(style='light-light')
        path = Path(__file__)
        current_path = path.with_stem(path.stem + '_3_layer_1').with_suffix('.xml')
        score.export_xml(path=current_path)
        """Not bad! Sam wants to create a measure for each duration.
        ...
        """

    def test_random_example_4_layer_1_measured(self):
        #################
        pool = [1, 2, 3, 4, 5]
        seed = 10
        periodicity = 3
        r = Random(pool=pool, seed=seed, periodicity=periodicity)
        proportions = [next(r) for _ in range(len(pool))]  # [5, 1, 4, 2, 3]
        tempo_1 = 5 * 6  # 30 the slowest tempo (5)
        tempo_2 = 5 * 5 * 6  # 150 the fastest tempo (1)
        all_tempi = [tempo_1 + (tempo_2 - tempo_1) * i / 4 for i in range(5)]  # a simple arithmetic progression
        section_quarter_duration = 5 * 4

        layer_1_proportions = [[r.__next__() for _ in range(5)] for x in range(5)]
        # [[1, 5, 4, 3, 1], [2, 4, 5, 3, 2], [4, 5, 1, 2, 3], [5, 4, 1, 3, 5], [2, 4, 1, 3, 5]]
        layer_1_quarter_durations = [
            [(Fraction(p, sum(layer_1_proportions[i]))) * section_quarter_duration for p in layer_1_proportions[i]]
            for i in range(5)]
        #################
        """Not bad! Sam wants to create a measure for each duration. That's not so easy: the quantization takes place 
        inside beats. It means chords must be added to a part and split (and tied) beatwise inside each measure 
        before quantizing. That's why after quantizing we cannot change measures anymore. It would be nice to have a 
        utility function to calculate quantized durations regardless of chords and parts. Unfortunately musicscore 
        does not provide such a function. :(
        Sam thinks of a work around for now ...
        """

        quantized_quarter_durations = [sams_get_quantized_durations(section, possible_subdivisions=[2]) for section in
                                       layer_1_quarter_durations]
        all_tempi = [all_tempi[p - 1] for p in proportions]

        score = Score()
        part = score.add_part('part_1')
        for section, tempo in zip(quantized_quarter_durations, all_tempi):
            chords = SimpleFormat(quarter_durations=section).chords
            chords[0].metronome = Metronome(tempo)
            for ch in chords:
                ch.add_lyric(f'{round(float(ch.quarter_duration) * 60 / tempo, 2)}"')
                time_signature = (ch.quarter_duration.numerator, 8) if ch.quarter_duration.denominator == 2 else (
                    ch.quarter_duration.numerator, 4)
                part.add_measure(time=time_signature)
                part.add_chord(ch)
            part.get_current_measure().set_barline(style='light-light')
        path = Path(__file__)
        current_path = path.with_stem(path.stem + '_4_layer_1_measured').with_suffix('.xml')
        score.export_xml(path=current_path)
        """
        Ok! It's getting somewhere!
        """
