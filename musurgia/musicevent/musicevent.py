from fractions import Fraction
from typing import Any

from musicscore import QuarterDuration, Chord, Metronome

from musurgia.musurgia_types import check_type


def calculate_duration(quarter_duration: QuarterDuration, tempo: Metronome) -> Fraction:
    return Fraction(60 / (tempo.per_minute / tempo.beat_unit) * quarter_duration)


class MusicEvent(Chord):
    _ATTRIBUTES = Chord._ATTRIBUTES.union({'tempo'})

    def __init__(self, quarter_duration: QuarterDuration, tempo: Metronome = Metronome(60), *args: Any, **kwargs: Any):  # type: ignore[no-untyped-call]
        super().__init__(quarter_duration=quarter_duration, *args, **kwargs)  # type: ignore
        self._tempo: Metronome
        self.tempo = tempo

    @property
    def tempo(self) -> Metronome:
        return self._tempo

    @tempo.setter
    def tempo(self, val: Metronome) -> None:
        check_type(val, Metronome, class_name=self.__class__.__name__, property_name='tempo')
        self._tempo = val

    def get_duration(self) -> Fraction:
        return calculate_duration(self.quarter_duration, self.tempo)
