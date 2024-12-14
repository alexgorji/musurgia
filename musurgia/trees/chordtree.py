from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Optional

from musurgia.timing.duration import Duration, convert_duration_to_quarter_duration_value
from musurgia.trees.timelinetree import TimelineTree
from musicscore.chord import Chord
from musicscore.metronome import Metronome
from musicscore.quarterduration import QuarterDuration

class EnsureInitializationMetaclass(ABCMeta):
    def __call__(cls, *args, **kwds):
        instance = super().__call__(*args, **kwds)
        if not getattr(instance, "_chord_initialized", False):
            raise RuntimeError(f"The method 'initialize_chord' was not called in {cls.__name__}!")
        return instance
    
class AbstractChordFactory(ABC, metaclass=EnsureInitializationMetaclass):
    # Create a Chord object with proper quarter_duration depending on Duration and Metronome objects
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._chord: "Chord"
        self._chord_initialized = False
        # Call initialize_chord in inherited classes

    
    def initiliaze_chord(self) -> None:
        quarter_duration = QuarterDuration(convert_duration_to_quarter_duration_value(self.get_metronome(), self.get_duration()))
        self._chord = Chord(60, quarter_duration=quarter_duration)
        self._chord_initialized = True

    def update_chord_quarter_duration(self):
        self._chord.quarter_duration.value = convert_duration_to_quarter_duration_value(self.get_metronome(), self.get_duration())

    @abstractmethod
    def get_duration(self) -> "Duration":
        pass

    @abstractmethod
    def get_metronome(self) -> "Metronome":
        pass

    @abstractmethod
    def get_chord(self) -> "Chord":
        pass

class ChordFactory(AbstractChordFactory):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._duration: "Duration" = Duration(1)
        self._metronome: "Metronome" = Metronome(60)
        self.initiliaze_chord()

    @property
    def duration(self):
        return self._duration
    
    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def metronome(self):
        return self._metronome
    
    @metronome.setter
    def metronome(self, value):
        self._metronome = value

    def get_chord(self) -> "Chord":
        self.update_chord_quarter_duration()
        return self._chord
    
    def get_duration(self) -> "Duration":
        return self._duration
    
    def get_metronome(self) -> "Metronome":
        return self._metronome
    

class TreeChordFactory(AbstractChordFactory):
    def __init__(self, chord_tree: "ChordTree", *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._chord_tree = chord_tree
        self.initiliaze_chord()


    def get_duration(self) -> "Duration":
        return self._chord_tree.get_duration()
    
    def get_metronome(self) -> "Duration":
        return self._chord_tree.get_metronome()
    
    def get_chord(self) -> "Chord":
        self.update_chord_quarter_duration()
        return self._chord
    

class ChordTree(TimelineTree):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._metronome = Metronome(60)
        self._chord_factory: "TreeChordFactory" = TreeChordFactory(self)

    @property
    def chord_factory(self) -> "TreeChordFactory":
        return self._chord_factory
    
    @property
    def chord(self):
        raise AttributeError("Use chord_factory for updating the chord")
    
    @chord.setter
    def chord(self, value: Any):
        raise AttributeError("Use get_chord() instead.")

    @property
    def metronome(self) -> "Metronome":
        return self._metronome
    
    @metronome.setter
    def metronome(self, value: "Metronome") -> None:
        self._metronome = value

    def get_chord(self) -> "Chord":
        return self.chord_factory.get_chord()
    
    def get_metronome(self)-> "Metronome":
        return self.metronome
    