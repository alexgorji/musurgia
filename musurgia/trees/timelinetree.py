from fractions import Fraction
from typing import Any, Union

from musurgia.timing.duration import ReadonlyDuration
from musurgia.trees.valuedtree import ValuedTree
from musurgia.musurgia_types import ConvertibleToFraction

__all__ = ["TimelineDuration", "TimelineTree"]

class TimelineDuration(ReadonlyDuration):
    def _set_seconds(self, seconds: ConvertibleToFraction) -> None:
        self._set_clock(hours=0, minutes=0, seconds=seconds)


class TimelineTree(ValuedTree):
    def __init__(self, duration: Union[TimelineDuration, ConvertibleToFraction], *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        if not isinstance(duration, TimelineDuration):
            duration = TimelineDuration(duration)
        self._duration: TimelineDuration = duration

    # private methods
    def _check_child_to_be_added(self, child: 'TimelineTree') -> bool:
        if not isinstance(child, TimelineTree):
            raise TypeError(f'Wrong child type. Child must be of type FractalTree not {type(child)}')
        return True

    def _set_value(self, value: ConvertibleToFraction) -> None:
        if not isinstance(value, Fraction):
            value = Fraction(value)
        self._duration._set_seconds(value)

    @property
    def duration(self) -> None:
        raise AttributeError("Use get_duration() instead.")
    
    def get_duration(self) -> TimelineDuration:
        return self._duration
    
    def get_value(self) -> Fraction:
        return self.get_duration().calculate_in_seconds()
    
    def update_duration(self, duration: Union[TimelineDuration, ConvertibleToFraction]) -> None:
        if isinstance(duration, TimelineDuration):
            self._duration = duration
            new_value = self.get_value()
        elif isinstance(duration, Fraction):
            new_value = duration
        else:
            new_value = Fraction(duration)
        self.update_value(new_value)

    

    
    