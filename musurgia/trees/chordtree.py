# from abc import ABC, ABCMeta, abstractmethod
# from typing import Any, Optional

# from musurgia.timing.duration import Duration, convert_duration_to_quarter_duration_value
# from musurgia.trees.timelinetree import TimelineTree
# from musicscore.chord import Chord # type: ignore
# from musicscore.metronome import Metronome # type: ignore
# from musicscore.quarterduration import QuarterDuration # type: ignore

# class EnsureInitializationMetaclass(ABCMeta):
#     def __call__(cls, *args: Any, **kwargs: Any) -> Any:
#         instance = super().__call__(*args, **kwargs)
#         if not getattr(instance, "_chord_initialized", False):
#             raise RuntimeError(f"The method 'initialize_chord' was not called in {cls.__name__}!")
#         return instance

# class AbstractChordFactory(ABC, metaclass=EnsureInitializationMetaclass):
#     # Create a Chord object with proper quarter_duration depending on Duration and Metronome objects
#     def __init__(self, *args: Any, **kwargs: Any):
#         super().__init__(*args, **kwargs)
#         self._chord: "Chord"
#         self._chord_initialized = False
#         # Call initialize_chord in inherited classes


#     def initiliaze_chord(self) -> None:
#         quarter_duration = QuarterDuration(convert_duration_to_quarter_duration_value(self.get_metronome(), self.get_duration()))
#         self._chord = Chord(60, quarter_duration=quarter_duration)
#         self._chord_initialized = True

#     def update_chord_quarter_duration(self) -> None:
#         self._chord.quarter_duration.value = convert_duration_to_quarter_duration_value(self.get_metronome(), self.get_duration())

#     @abstractmethod
#     def get_duration(self) -> "Duration":
#         pass

#     @abstractmethod
#     def get_metronome(self) -> "Metronome":
#         pass

#     @abstractmethod
#     def get_chord(self) -> "Chord":
#         pass

# class TreeChordFactory:
#     __CHORD_UPDATE_METHODS = {'_update_chord_quarter_duration'}

#     def __init__(self, chord_tree: "ChordTree", *args: Any, **kwargs: Any):
#         super().__init__(*args, **kwargs)
#         self._chord: Chord = Chord(60, 1)
#         self._chord_tree = chord_tree


#     def _update_chord_quarter_duration(self):
#         self._chord.quarter_duration.value = convert_duration_to_quarter_duration_value(self.get_metronome(), self.get_duration())

#     def _update_chord(self):
#         for method_name in self.__class__.__CHORD_UPDATE_METHODS:
#             getattr(self, method_name)

#     def get_duration(self) -> "Duration":
#         return self._chord_tree.get_duration()

#     def get_metronome(self) -> "Metronome":
#         return self._chord_tree.get_metronome()

#     def get_chord(self) -> "Chord":
#         self._update_chord()
#         return self._chord


# class ChordTree(TimelineTree):
#     def __init__(self, *args: Any, **kwargs: Any):
#         super().__init__(*args, **kwargs)
#         self._metronome = Metronome(60)
#         self._chord_factory: "TreeChordFactory" = TreeChordFactory(self)

#     @property
#     def chord(self):
#         raise AttributeError('Use get_chord() instead.')

#     @property
#     def chord(self, value):
#         raise AttributeError('Update self.chord_factory instead.')

#     @property
#     def chord_factory(self) -> "TreeChordFactory":
#         return self._chord_factory

#     @property
#     def metronome(self) -> "Metronome":
#         return self._metronome

#     @metronome.setter
#     def metronome(self, value: "Metronome") -> None:
#         self._metronome = value

#     def get_chord(self) -> "Chord":
#         return self.chord_factory.get_chord()

#     def get_metronome(self)-> "Metronome":
#         return self.metronome
