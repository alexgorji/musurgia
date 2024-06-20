from fractions import Fraction
from typing import Any, Union

from musicscore import QuarterDuration, Chord


class MusicEvent(Chord):
    def __init__(self, quarter_duration: QuarterDuration, tempo: Union[float, int] = 60, *args: Any, **kwargs: Any):
        super().__init__(quarter_duration=quarter_duration, *args, **kwargs)
        self._tempo: Union[float, int]
        self.tempo = tempo

    @property
    def tempo(self) -> Union[float, int]:
        return self._tempo

    @tempo.setter
    def tempo(self, val: Union[float, int]):
        self._tempo = val

    def get_duration(self) -> Fraction:
        pass
