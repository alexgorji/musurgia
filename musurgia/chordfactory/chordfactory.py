from abc import ABC, ABCMeta, abstractmethod
from typing import Any

from musicscore.chord import Chord  # type: ignore


class ChordFactoryType(ABCMeta):
    def __new__(mcls, name, bases, namespace, /, **kwargs):  # type: ignore
        chord_update_methods = {
            k for k in namespace.keys() if k.startswith("update_chord_")
        }

        for base in bases:
            base_methods = getattr(base, "_CHORD_UPDATE_METHODS", set())
            chord_update_methods.update(base_methods)

        namespace["_CHORD_UPDATE_METHODS"] = chord_update_methods
        return super().__new__(mcls, name, bases, namespace, **kwargs)


class AbstractChordFactory(ABC, metaclass=ChordFactoryType):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._chord: Chord = Chord(60, 1)

    def _update_chord(self) -> None:
        for method_name in self._CHORD_UPDATE_METHODS:  # type: ignore
            getattr(self, method_name)()

    @property
    def chord(self) -> None:
        raise AttributeError("Use get_chord() instead.")

    @chord.setter
    def chord(self, value: Any) -> None:
        raise AttributeError("ChordFactory.chord cannot be set. ")

    @abstractmethod
    def update_chord_quarter_duration(self) -> None:
        pass

    @abstractmethod
    def update_chord_midis(self) -> None:
        pass

    def get_chord(self) -> "Chord":
        self._update_chord()
        return self._chord