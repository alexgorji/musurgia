from fractions import Fraction
from typing import Any

from musurgia.musurgia_exceptions import WrongNodeDurationError
from musurgia.timing.duration import Duration
from musurgia.trees.valuedtree import ValuedTree
from musurgia.musurgia_types import ConvertibleToFraction

__all__ = ["TimelineTree"]


class TimelineTree(ValuedTree):
    def __init__(self, duration: Duration, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._duration: Duration = duration

    # private methods
    def _check_child_to_be_added(self, child: 'TimelineTree') -> bool:
        if not isinstance(child, TimelineTree):
            raise TypeError(f'Wrong child type. Child must be of type FractalTree not {type(child)}')
        return True

    def _set_value(self, value: ConvertibleToFraction) -> None:
        self._duration.seconds = float(value)

    def check_timeline_durations(self) -> bool:
        for ch in self.traverse():
            if not ch.is_leaf:
                if sum([gch.get_duration() for gch in ch.get_children()]) != ch.get_duration():
                    raise WrongNodeDurationError(f"Children of TimelineTree node of position {ch.get_position_in_tree()} with duration {ch.get_duration().seconds} have wrong durations {[gch.get_duration().seconds for gch in ch.get_children()]} ")
        return True

    def get_duration(self) -> Duration:
        return self._duration
    
    def get_value(self) -> Fraction:
        return Fraction(self.get_duration().seconds)
    

    
    