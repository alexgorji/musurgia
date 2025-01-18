from abc import abstractmethod
from copy import deepcopy
from itertools import cycle
from typing import Any, Iterator, Optional, TypeVar, cast

from musicscore.midi import Midi
from musicscore.score import Score
from musurgia.chordfactory.chordfactory import AbstractChordFactory
from musurgia.magicrandom import MagicRandom
from musurgia.musurgia_exceptions import (
    RelativeTreeChordFactoryHasNoMidiValueRangeError,
)
from musurgia.trees.fractaltimelinetree import FractalTimelineTree
from musurgia.trees.timelinetree import TimelineTree
from musurgia.utils import RelativeValueGenerator
from musurgia.musurgia_types import MidiValue, MidiValueMicroTone, DirectionValue


class TreeChordFactory(AbstractChordFactory):
    def __init__(
        self,
        musical_tree_node: "MusicalTree",
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self._musical_tree_node: "MusicalTree" = musical_tree_node
        self._show_metronome: bool = False
        self._midis = [Midi(72)]

    @property
    def midis(self) -> list[Midi]:
        return self._midis

    @midis.setter
    def midis(self, value: list[Midi]) -> None:
        self._midis = value

    @property
    def show_metronome(self) -> bool:
        return self._show_metronome

    @show_metronome.setter
    def show_metronome(self, value: bool) -> None:
        self._show_metronome = value

    def get_midis(self) -> list[Midi]:
        return self.midis

    def get_musical_tree_node(self) -> "MusicalTree":
        return self._musical_tree_node

    def update_chord_quarter_duration(self) -> None:
        self._chord.quarter_duration = deepcopy(
            self.get_musical_tree_node().get_duration().get_quarter_duration()
        )

    def update_chord_midis(self) -> None:
        self._chord.midis = deepcopy(self.get_midis())

    def update_chord_metronome(self) -> None:
        if self.show_metronome:
            self._chord.metronome = (
                self.get_musical_tree_node().get_duration().get_metronome()
            )
        else:
            self._chord._metronome = None


class TreeMidiGenerator:
    def __init__(self, musical_tree_node: "MusicalTree", *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._musical_tree_node: "MusicalTree" = musical_tree_node

    @abstractmethod
    def set_musical_tree_midis(self) -> None:
        pass

    def get_musical_tree_node(self) -> "MusicalTree":
        return self._musical_tree_node


class MagicRandomTreeMidiGenerator(TreeMidiGenerator, MagicRandom):
    def set_musical_tree_midis(self) -> None:
        for node in self._musical_tree_node.traverse():
            node.get_chord_factory().midis = next(self)


class RelativeTreeChordFactory(TreeChordFactory):
    def __init__(
        self,
        midi_value_range: Optional[tuple[MidiValue, MidiValue]] = None,
        micro_tone: MidiValueMicroTone = MidiValueMicroTone.HALF,
        direction_iterator: Optional[Iterator[DirectionValue]] = None,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self._midi_value_range: Optional[tuple[MidiValue, MidiValue]]
        self._micro_tone: MidiValueMicroTone
        self._direction_iterator: Optional[Iterator[DirectionValue]]

        self.midi_value_range = midi_value_range
        self.micro_tone = micro_tone
        self.direction_iterator = direction_iterator

    @property
    def micro_tone(self) -> MidiValueMicroTone:
        return self._micro_tone

    @micro_tone.setter
    def micro_tone(self, value: MidiValueMicroTone) -> None:
        self._micro_tone = value

    @property
    def midi_value_range(self) -> Optional[tuple[MidiValue, MidiValue]]:
        return self._midi_value_range

    @midi_value_range.setter
    def midi_value_range(self, value: Optional[tuple[MidiValue, MidiValue]]) -> None:
        self._midi_value_range = value

    @property
    def direction_iterator(self) -> Optional[Iterator[DirectionValue]]:
        if not self._direction_iterator:
            self._direction_iterator = cycle([1, -1])
        return self._direction_iterator

    @direction_iterator.setter
    def direction_iterator(self, value: Optional[Iterator[DirectionValue]]) -> None:
        self._direction_iterator = value


class RelativeTreeMidiGenerator(TreeMidiGenerator):
    def set_musical_tree_midis(self) -> None:
        if not isinstance(
            self.get_musical_tree_node().get_chord_factory(), RelativeTreeChordFactory
        ):
            raise TypeError

        if not cast(
            RelativeTreeChordFactory, self.get_musical_tree_node().get_chord_factory()
        ).midi_value_range:
            children_ranges = [
                cast(
                    RelativeTreeChordFactory, child.get_chord_factory()
                ).midi_value_range
                for child in self.get_musical_tree_node().get_children()
            ]
            if not children_ranges or None in children_ranges:
                raise RelativeTreeChordFactoryHasNoMidiValueRangeError()
            else:
                cast(
                    RelativeTreeChordFactory,
                    self.get_musical_tree_node().get_chord_factory(),
                ).midi_value_range = (
                    0,
                    0,
                )

        for node in self.get_musical_tree_node().traverse():
            if not node.is_leaf:
                node_chord_factory = node.get_chord_factory()
                children = node.get_children()
                proportions = [ch.get_value() for ch in children]
                directions = [
                    next(node_chord_factory.direction_iterator)
                    for _ in range(len(proportions))
                ]
                children_midi_value_ranges = list(
                    RelativeValueGenerator(
                        value_range=node_chord_factory.midi_value_range,
                        directions=directions,
                        proportions=proportions,
                        value_grid=node_chord_factory.micro_tone.value,
                    )
                )
                for index in range(len(children_midi_value_ranges) - 1):
                    child = children[index]
                    if child.get_chord_factory().midi_value_range is None:
                        min_midi = float(children_midi_value_ranges[index])
                        max_midi = float(children_midi_value_ranges[index + 1])
                        children[index].get_chord_factory().midi_value_range = (
                            min_midi,
                            max_midi,
                        )

                    min_midi, _ = child.get_chord_factory().midi_value_range

                    children[index].get_chord_factory().midis = [Midi(min_midi)]


class MusicalTree(TimelineTree):
    DEFAULT_TREE_CHORD_FACTORY = TreeChordFactory

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._tree_chord_factory: TreeChordFactory
        self.set_tree_chord_factory_class(self.DEFAULT_TREE_CHORD_FACTORY)

    def set_tree_chord_factory_class(self, value: type[TreeChordFactory]) -> None:
        self._tree_chord_factory = value(musical_tree_node=self)

    def get_chord_factory(self) -> TreeChordFactory:
        return self._tree_chord_factory

    def export_score(self) -> Score:
        score = Score()
        for layer_number in range(1, self.get_number_of_layers() + 1):
            part = score.add_part(f"part-{layer_number + 1}")
            layer = self.get_layer(level=layer_number)
            for node in layer:
                part.add_chord(node.get_chord_factory().create_chord())
        return score


T = TypeVar("T", bound="FractalMusicalTree")


class FractalMusicalTree(FractalTimelineTree, MusicalTree):
    def split(self: "T", *proportions: Any) -> list["T"]:
        children = super().split(*proportions)
        for child in children:
            child._tree_chord_factory = deepcopy(self._tree_chord_factory)
        return children


class RelativeMusicTree(MusicalTree):
    DEFAULT_TREE_CHORD_FACTORY = RelativeTreeChordFactory


class FractalDirectionIterator:
    DEFAULT_MAIN_DIRECTION_CELL: list[DirectionValue] = [1, -1]

    def __init__(
        self,
        main_direction_cell: Optional[list[DirectionValue]],
        fractal_node: "FractalRelativeMusicTree",
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self._fractal_node: FractalRelativeMusicTree = fractal_node
        self._main_direction_cell: Optional[list[DirectionValue]] = main_direction_cell
        self._iter_index = -1

    @property
    def main_direction_cell(self) -> Optional[list[DirectionValue]]:
        if self._main_direction_cell is None:
            if self._fractal_node.up is None:
                return self.DEFAULT_MAIN_DIRECTION_CELL
            else:
                return cast(
                    Optional[list[DirectionValue]],
                    self._fractal_node.up.get_chord_factory().direction_iterator.main_direction_cell,
                )
        else:
            return self._main_direction_cell

    @main_direction_cell.setter
    def main_direction_cell(self, value: Optional[list[DirectionValue]]) -> None:
        self._main_direction_cell = value

    def reset(self) -> None:
        self._iter_index = -1

    def get_directions(self) -> list[DirectionValue]:
        fractal_orders = [
            ch.get_fractal_order() for ch in self._fractal_node.get_children()
        ]
        return [self.get_main_directions()[fo - 1] for fo in fractal_orders]

    def get_main_directions(self) -> list[DirectionValue]:
        cy = cycle(cast(list[DirectionValue], self.main_direction_cell))
        return [next(cy) for _ in range(len(self._fractal_node.proportions))]

    def __iter__(self) -> Iterator[DirectionValue]:
        return self

    def __next__(self) -> DirectionValue:
        try:
            self._iter_index += 1
            return self.get_directions()[self._iter_index]
        except IndexError:
            raise StopIteration


class FractalRelativeTreeChordFactory(RelativeTreeChordFactory):
    def __init__(
        self,
        main_direction_cell: Optional[list[DirectionValue]] = None,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.direction_iterator = FractalDirectionIterator(
            main_direction_cell=main_direction_cell,
            fractal_node=cast(FractalRelativeMusicTree, self.get_musical_tree_node()),
        )


class FractalRelativeMusicTree(FractalMusicalTree, RelativeMusicTree):
    DEFAULT_TREE_CHORD_FACTORY = FractalRelativeTreeChordFactory
