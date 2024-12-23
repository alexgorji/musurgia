from abc import abstractmethod
from copy import deepcopy
from typing import Any

from musicscore.midi import Midi  # type: ignore
from musicscore.score import Score  # type: ignore
from musurgia.chordfactory.chordfactory import AbstractChordFactory
from musurgia.trees.timelinetree import TimelineTree


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


# class TreeMidiGeneratorMixin:
#     def __init__(self, root_midis: list[Midi] = [Midi(72)], *args: Any, **kwargs: Any):
#         super().__init__(*args, **kwargs)
#         self._root_midis = root_midis
#         self._children_midi_generator: MidiGenerator
#         self._midis: list[Midi]

#     @property
#     def children_midi_generator(self) -> MidiGenerator:
#         return self._children_midi_generator

#     @children_midi_generator.setter
#     def children_midi_generator(self, value: MidiGenerator) -> None:
#         self._children_midi_generator = value

#     def get_children_midi_generator(self):
#         try:
#             return self._children_midi_generator
#         except AttributeError:
#             self._children_midi_generator = OneMidiGenerator(72)
#             return self._children_midi_generator

#     def get_midis(self):
#         return [72]
#         # try:
#         #     return self._midis
#         # except AttributeError:
#         #     if self.is_root:
#         #         self._midis = self._root_midis
#         #     else:
#         #         parent = self.get_parent()
#         #         for node in parent.get_children():
#         #             node._midis = next(parent.get_children_midi_generator())
#         # return self._midis


# class RelativeMidiGeneratorMixin:
#     def __init__(self, *args: Any, **kwargs: Any):
#         super().__init__(*args, **kwargs)


class OneToneTreeChordFactory(TreeChordFactory):
    def __init__(self, midi: Midi, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._midi = midi

    def update_chord_midis(self) -> None:
        self._chord.midis = deepcopy([self._midi])


class SimpleMusicalTree(MusicalTree):
    def __init__(self, midi: Midi=Midi(72), *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._tree_chord_factory: TreeChordFactory = OneToneTreeChordFactory(
            midi=midi, musical_tree_node=self
        )

    def get_chord_factory(self) -> TreeChordFactory:
        return self._tree_chord_factory
