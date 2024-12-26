from abc import abstractmethod
from copy import deepcopy
from enum import Enum
from itertools import cycle
from typing import Any, Iterator, Literal, Optional, Union

from musicscore.midi import Midi
from musicscore.score import Score
from musurgia.chordfactory.chordfactory import AbstractChordFactory
from musurgia.trees.fractaltimelinetree import FractalTimelineTree
from musurgia.trees.timelinetree import TimelineTree
from musurgia.utils import RelativeValueGenerator


class TreeChordFactory(AbstractChordFactory):
    def __init__(
        self,
        musical_tree_node: "MusicalTree",
        show_metronome: bool = False,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self._musical_tree_node: "MusicalTree" = musical_tree_node
        self._show_metronome: bool
        self.show_metronome = show_metronome

    @property
    def show_metronome(self) -> bool:
        return self._show_metronome

    @show_metronome.setter
    def show_metronome(self, value: bool) -> None:
        self._show_metronome = value

    def get_musical_tree_node(self) -> "MusicalTree":
        return self._musical_tree_node

    def update_chord_quarter_duration(self) -> None:
        self._chord.quarter_duration = deepcopy(
            self.get_musical_tree_node().get_duration().get_quarter_duration()
        )

    @abstractmethod
    def update_chord_midis(self) -> None:
        pass

    def update_chord_metronome(self) -> None:
        if self.show_metronome:
            self._chord.metronome = (
                self.get_musical_tree_node().get_duration().get_metronome()
            )
        else:
            self._chord._metronome = None


class MusicalTree(TimelineTree):
    @abstractmethod
    def get_chord_factory(self) -> TreeChordFactory:
        pass

    def export_score(self) -> Score:
        score = Score()
        for layer_number in range(self.get_number_of_layers() + 1):
            part = score.add_part(f"part-{layer_number + 1}")
            layer = self.get_layer(level=layer_number)
            for node in layer:
                part.add_chord(node.get_chord_factory().create_chord())
        return score


class MidiMusicalTreeChordFactory(TreeChordFactory):
    def __init__(
        self, midis: list[Midi] = [Midi(72)], *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self._midis: list[Midi]
        self.midis = midis

    def update_chord_midis(self) -> None:
        self._chord.midis = deepcopy(self.get_midis())

    @property
    def midis(self) -> list[Midi]:
        return self._midis

    @midis.setter
    def midis(self, value: list[Midi]) -> None:
        self._midis = value

    def get_midis(self) -> list[Midi]:
        return self.midis


class MidiMusicalTree(MusicalTree):
    def __init__(
        self, midis: list[Midi] = [Midi(72)], *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self._tree_chord_factory: MidiMusicalTreeChordFactory = (
            MidiMusicalTreeChordFactory(musical_tree_node=self, midis=midis)
        )

    def get_chord_factory(self) -> TreeChordFactory:
        return self._tree_chord_factory


class FractalMusicalTree(FractalTimelineTree, MidiMusicalTree):
    pass


MidiValue = Union[int, float]


class MidiValueMicroTone(Enum):
    HALF = 1.0
    QUARTER = 0.5
    EIGHT = 0.25

DirectionValue = Literal[-1, 1]

class RelativeMusicTree(MusicalTree):
    TreeChordFactoryClass = MidiMusicalTreeChordFactory

    def __init__(
        self,
        midi_value_range: Optional[tuple[MidiValue]] = None,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self._midi_value_range: Optional[tuple[MidiValue]] = midi_value_range
        self._micro_tone: MidiValueMicroTone = MidiValueMicroTone.HALF
        self._direction_iterator: Iterator[DirectionValue] = cycle([-1, 1])
        self._tree_chord_factory = (
            self.TreeChordFactoryClass(musical_tree_node=self)
        )

    @property
    def micro_tone(self) -> MidiValueMicroTone:
        return self._micro_tone

    @micro_tone.setter
    def micro_tone(self, value: MidiValueMicroTone) -> None:
        self._micro_tone = value

    @property
    def midi_value_range(self) -> Optional[tuple[MidiValue]]:
        return self._midi_value_range

    @midi_value_range.setter
    def midi_value_range(self, value: Optional[tuple[MidiValue]]) -> None:
        self._midi_value_range = value

    @property
    def direction_iterator(self) -> Iterator[DirectionValue]:
        return self._direction_iterator

    @direction_iterator.setter
    def direction_iterator(self, value: Iterator[DirectionValue]) -> None:
        self._direction_iterator = value

    def get_chord_factory(self) -> TreeChordFactory:
        return self._tree_chord_factory

    def set_relative_midis(self) -> None:
        if not self.midi_value_range:
            raise AttributeError("set_relative_midis: midi_value_range cannot be None.")
        for node in self.traverse():
            node.get_chord_factory().midis = [Midi(node.midi_value_range[0])]
            if not node.is_leaf:
                children = node.get_children()
                proportions = [ch.get_value() for ch in children]
                directions = [
                    next(node.direction_iterator) for _ in range(len(proportions))
                ]
                children_midi_value_ranges = list(
                    RelativeValueGenerator(
                        value_range=node.midi_value_range,
                        directions=directions,
                        proportions=proportions,
                        value_grid=self.micro_tone.value,
                    )
                )
                for index in range(len(children_midi_value_ranges) - 1):
                    min_midi = float(children_midi_value_ranges[index])
                    max_midi = float(children_midi_value_ranges[index + 1])
                    children[index].midi_value_range = (min_midi, max_midi)


class FractalDirectionIterator:
    def __init__(self, main_direction_cell: list[DirectionValue], fractal_node: FractalTimelineTree, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._fractal_node: FractalTimelineTree = fractal_node
        self._main_direction_cell: list[DirectionValue] = main_direction_cell
        self._iter_index = -1

    def reset(self) -> None:
        self._iter_index = -1

    def get_directions(self) -> list[DirectionValue]:
        fractal_orders = [
            ch.get_fractal_order() for ch in self._fractal_node.get_children()
        ]
        return [self.get_main_directions()[fo - 1] for fo in fractal_orders]

    def get_main_directions(self) -> list[DirectionValue]:
        cy = cycle(self._main_direction_cell)
        return [next(cy) for _ in range(len(self._fractal_node.proportions))]

    def __iter__(self) -> Iterator[DirectionValue]:
        return self

    def __next__(self) -> DirectionValue:
        try:
            self._iter_index += 1
            return self.get_directions()[self._iter_index]
        except IndexError:
            raise StopIteration


class FractalRelativeMusicTree(FractalTimelineTree, RelativeMusicTree):
    def __init__(self, main_direction_cell: list[DirectionValue]=[1, -1], *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._direction_iterator = FractalDirectionIterator(
            main_direction_cell=main_direction_cell, fractal_node=self
        )
