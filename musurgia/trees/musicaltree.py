from abc import ABC, abstractmethod
from typing import Any

from musicscore.chord import Chord  # type: ignore
from musicscore.midi import Midi  # type: ignore
from musicscore.score import Score  # type: ignore
from musurgia.trees.timelinetree import TimelineTree


class AbstractMusicalTree(TimelineTree, ABC):
    def __init__(self, show_metronome: bool = False, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._show_metronome: bool
        self.show_metronome = show_metronome

    @property
    def show_metronome(self) -> bool:
        return self._show_metronome

    @show_metronome.setter
    def show_metronome(self, value: bool) -> None:
        self._show_metronome = value

    @abstractmethod
    def get_midis(self) -> list[Midi]:
        pass

    def create_chord(self) -> Chord:
        chord = Chord(
            midis=self.get_midis(),
            quarter_duration=self.get_duration().get_quarter_duration(),
        )
        if self.show_metronome:
            chord.metronome = self.get_duration().get_metronome()
        return chord

    def export_score(self) -> Score:
        score = Score()
        for layer_number in range(self.get_number_of_layers() + 1):
            part = score.add_part(f"part-{layer_number + 1}")
            layer = self.get_layer(level=layer_number)
            for node in layer:
                part.add_chord(node.create_chord())
        return score


class SimpleMusicalTree(AbstractMusicalTree):
    def get_midis(self) -> list[Midi]:
        return [Midi(72)]

