from fractions import Fraction
from typing import Any

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
        self._duration.seconds = Fraction(value)

    def get_duration(self) -> Duration:
        return self._duration
    
    def get_value(self) -> Fraction:
        return self.get_duration().calculate_in_seconds()
    

    
    