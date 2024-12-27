from abc import ABC, abstractmethod
from fractions import Fraction
from typing import Any, Iterator, Literal, Union

from musicscore.midi import Midi
from musurgia.magicrandom import MagicRandom
from musurgia.utils import RelativeValueGenerator


class MidiGenerator(ABC):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    @abstractmethod
    def __next__(self) -> Midi:
        pass


class OneMidiGenerator(MidiGenerator):
    def __init__(self, midi_value: Union[float, int], *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._midi_value = midi_value

    def __next__(self) -> Midi:
        return Midi(self._midi_value)


class RandomMidiGenerator(MagicRandom, MidiGenerator):
    def __next__(self) -> Midi:
        return Midi(float(super().__next__()))


MicrotoneValueTypes = Literal[2, 4, 8]


class RelativeMidiGenerator(RelativeValueGenerator, MidiGenerator):
    def __init__(self, microtone: MicrotoneValueTypes = 2, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._microtone: MicrotoneValueTypes
        self.microtone = microtone

    @property
    def microtone(self) -> MicrotoneValueTypes:
        return self._microtone

    @microtone.setter
    def microtone(self, value: MicrotoneValueTypes) -> None:
        if value not in [2, 4, 8]:
            raise ValueError("RelativeMidiGenerator.microtone can only be 2, 4 or 8.")
        self._microtone = value
        self.value_grid = Fraction(1, (value // 2))

    def _midi_generator(self) -> Iterator[Midi]:
        for val in self.get_values():
            yield Midi(float(val))

    def __iter__(self) -> Iterator[Midi]:
        self._generator = self._midi_generator()
        return self

    def __next__(self) -> Midi:
        return next(self._generator)
