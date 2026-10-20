from abc import abstractmethod
from copy import deepcopy
from itertools import cycle
from typing import Any, Generic, Iterator, Sequence, Type, TypeVar, cast

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

TCF = TypeVar("TCF", bound="TreeChordFactory")


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

    def create_copy(self: TCF, musical_tree_node: "MusicalTree") -> "TCF":
        new_instance = self.__class__(musical_tree_node=musical_tree_node)
        new_instance._show_metronome = self._show_metronome
        new_instance.midis = deepcopy(self._midis)
        return new_instance


NodeT = TypeVar("NodeT", bound="MusicalTree")


class TreeMidiGenerator(Generic[NodeT]):
    def __init__(self, musical_tree_node: NodeT, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._musical_tree_node: NodeT = musical_tree_node

    @abstractmethod
    def set_musical_tree_midis(self) -> None:
        pass

    def get_musical_tree_node(self) -> NodeT:
        return self._musical_tree_node


class MagicRandomTreeMidiGenerator(TreeMidiGenerator["MusicalTree"], MagicRandom):
    def set_musical_tree_midis(self) -> None:
        for node in self._musical_tree_node.traverse():
            node.get_chord_factory().midis = next(self)


class RelativeTreeChordFactory(TreeChordFactory):
    def __init__(
        self,
        midi_value_range: tuple[MidiValue, MidiValue] | None = None,
        micro_tone: MidiValueMicroTone = MidiValueMicroTone.HALF,
        direction_iterator: Iterator[DirectionValue] | None = None,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self._midi_value_range: tuple[MidiValue, MidiValue] | None
        self._micro_tone: MidiValueMicroTone
        self._direction_iterator: Iterator[DirectionValue] | None
        self._include_last_midi_in_range: bool = False

        self.midi_value_range = midi_value_range
        self.micro_tone = micro_tone
        self.direction_iterator = direction_iterator

    @property
    def include_last_midi_in_range(self) -> bool:
        return self._include_last_midi_in_range

    @include_last_midi_in_range.setter
    def include_last_midi_in_range(self, value: bool) -> None:
        self._include_last_midi_in_range = value

    @property
    def micro_tone(self) -> MidiValueMicroTone:
        return self._micro_tone

    @micro_tone.setter
    def micro_tone(self, value: MidiValueMicroTone) -> None:
        self._micro_tone = value

    @property
    def midi_value_range(self) -> tuple[MidiValue, MidiValue] | None:
        return self._midi_value_range

    @midi_value_range.setter
    def midi_value_range(self, value: tuple[MidiValue, MidiValue] | None) -> None:
        self._midi_value_range = value

    @property
    def direction_iterator(self) -> Iterator[DirectionValue] | None:
        if not self._direction_iterator:
            self._direction_iterator = cycle([1, -1])
        return self._direction_iterator

    @direction_iterator.setter
    def direction_iterator(self, value: Iterator[DirectionValue] | None) -> None:
        self._direction_iterator = value

    def create_copy(
        self, musical_tree_node: "MusicalTree"
    ) -> "RelativeTreeChordFactory":
        new_instance = super().create_copy(musical_tree_node)
        new_instance._midi_value_range = deepcopy(self._midi_value_range)
        new_instance._micro_tone = deepcopy(self._micro_tone)
        if isinstance(
            self._direction_iterator, FractalDirectionIterator
        ) and isinstance(musical_tree_node, FractalRelativeMusicTree):
            new_instance._direction_iterator = self._direction_iterator.create_copy(
                musical_tree_node
            )
        else:
            new_instance._direction_iterator = deepcopy(self._direction_iterator)
        return new_instance


class RelativeTreeMidiGenerator(TreeMidiGenerator["RelativeMusicTree"]):
    def set_musical_tree_midis(self) -> None:
        if not self.get_musical_tree_node().get_chord_factory().midi_value_range:
            children_ranges = [
                child.get_chord_factory().midi_value_range
                for child in self.get_musical_tree_node().get_children()
            ]
            if not children_ranges or None in children_ranges:
                raise RelativeTreeChordFactoryHasNoMidiValueRangeError()
            else:
                self.get_musical_tree_node().get_chord_factory().midi_value_range = (
                    0,
                    0,
                )

        for node in self.get_musical_tree_node().traverse():
            if not node.is_leaf:
                node_chord_factory = node.get_chord_factory()

                children = node.get_children()
                proportions = [ch.get_value() for ch in children]
                if not node_chord_factory.direction_iterator:
                    raise ValueError
                directions = [
                    next(node_chord_factory.direction_iterator)
                    for _ in range(len(proportions))
                ]
                if not node_chord_factory.midi_value_range:
                    raise ValueError
                children_midi_value_ranges = list(
                    RelativeValueGenerator(
                        value_range=node_chord_factory.midi_value_range,
                        directions=directions,
                        proportions=proportions,
                        value_grid=node_chord_factory.micro_tone.value,
                        include_last_midi_in_range=node_chord_factory.include_last_midi_in_range,
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
                    midi_range = child.get_chord_factory().midi_value_range
                    if not midi_range:
                        raise ValueError
                    min_midi, _ = midi_range

                    children[index].get_chord_factory().midis = [Midi(min_midi)]


class MusicalTree(TimelineTree):
    DEFAULT_TREE_CHORD_FACTORY = TreeChordFactory

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._tree_chord_factory: TreeChordFactory
        self.set_tree_chord_factory_class(self.DEFAULT_TREE_CHORD_FACTORY)

    def set_tree_chord_factory_class(self, value: type[TreeChordFactory]) -> None:
        """Replace the factory with the default factory type or one of its subclasses."""
        if not issubclass(value, self.DEFAULT_TREE_CHORD_FACTORY):
            raise TypeError(
                f"{type(self).__name__} requires a subclass of "
                f"{self.DEFAULT_TREE_CHORD_FACTORY.__name__}, got {value.__name__}"
            )
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
            child._tree_chord_factory = self._tree_chord_factory.create_copy(child)
        return children


class RelativeMusicTree(MusicalTree):
    DEFAULT_TREE_CHORD_FACTORY: Type[TreeChordFactory] = RelativeTreeChordFactory

    def get_chord_factory(self) -> RelativeTreeChordFactory:
        factory = super().get_chord_factory()
        if not isinstance(factory, RelativeTreeChordFactory):
            raise TypeError("RelativeMusicTree requires a RelativeTreeChordFactory")
        return factory


class FractalDirectionIterator:
    DEFAULT_MAIN_DIRECTION_CELL: list[DirectionValue] = [1, -1]

    def __init__(
        self,
        main_direction_cell: Sequence[DirectionValue] | None,
        fractal_node: "FractalRelativeMusicTree",
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self._fractal_node: FractalRelativeMusicTree = fractal_node
        self._main_direction_cell: Sequence[DirectionValue] | None = main_direction_cell
        self._iter_index = -1

    @property
    def main_direction_cell(self) -> Sequence[DirectionValue] | None:
        if self._main_direction_cell is None:
            if self._fractal_node.up is None:
                return self.DEFAULT_MAIN_DIRECTION_CELL
            else:
                return self._fractal_node.up.get_chord_factory().direction_iterator.main_direction_cell

        else:
            return self._main_direction_cell

    @main_direction_cell.setter
    def main_direction_cell(self, value: list[DirectionValue] | None) -> None:
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

    def create_copy(
        self, fractal_node: "FractalRelativeMusicTree"
    ) -> "FractalDirectionIterator":
        return self.__class__(
            main_direction_cell=self.main_direction_cell, fractal_node=fractal_node
        )


class FractalRelativeTreeChordFactory(RelativeTreeChordFactory):
    def __init__(
        self,
        main_direction_cell: Sequence[DirectionValue] | None = None,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.direction_iterator = FractalDirectionIterator(
            main_direction_cell=main_direction_cell,
            fractal_node=cast(FractalRelativeMusicTree, self.get_musical_tree_node()),
        )

    @property
    def direction_iterator(self) -> FractalDirectionIterator:
        if self._direction_iterator is None:
            node = self.get_musical_tree_node()
            if not isinstance(node, FractalRelativeMusicTree):
                raise TypeError(
                    "FractalRelativeTreeChordFactory requires a FractalRelativeMusicTree"
                )
            self._direction_iterator = FractalDirectionIterator(
                main_direction_cell=None, fractal_node=node
            )
        if not isinstance(self._direction_iterator, FractalDirectionIterator):
            raise TypeError(
                "FractalRelativeTreeChordFactory requires a FractalDirectionIterator"
            )
        return self._direction_iterator

    @direction_iterator.setter
    def direction_iterator(self, value: Iterator[DirectionValue] | None) -> None:
        """Accept a fractal iterator, or None to reset to inherited directions."""
        if value is not None and not isinstance(value, FractalDirectionIterator):
            raise TypeError(
                "FractalRelativeTreeChordFactory requires a FractalDirectionIterator"
            )
        self._direction_iterator = value


class FractalRelativeMusicTree(FractalMusicalTree, RelativeMusicTree):
    DEFAULT_TREE_CHORD_FACTORY = FractalRelativeTreeChordFactory

    def get_chord_factory(self) -> FractalRelativeTreeChordFactory:
        factory = super().get_chord_factory()
        if not isinstance(factory, FractalRelativeTreeChordFactory):
            raise TypeError(
                "FractalRelativeMusicTree requires a FractalRelativeTreeChordFactory"
            )
        return factory
