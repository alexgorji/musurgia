from abc import ABC, ABCMeta, abstractmethod
from typing import Any

from musicscore.chord import Chord


class ChordFactoryType(ABCMeta):
    def __new__(cls, name, bases, attrs):
        attrs["_CHORD_UPDATE_METHODS"] = {
            k: v for k, v in attrs.items() if k.startswith("update_chord_")
        }
        return super().__new__(cls, name, bases, attrs)


class AbstractChordFactory(ABC, metaclass=ChordFactoryType):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._chord: Chord = Chord(60, 1)

    @abstractmethod
    def update_chord_quarter_duration(self) -> None:
        pass

    @abstractmethod
    def update_chord_midis(self) -> None:
        pass

    def _update_chord(self) -> None:
        for method_name in self.__class__._CHORD_UPDATE_METHODS:
            getattr(self, method_name)()

    def get_chord(self) -> "Chord":
        self._update_chord()
        return self._chord
