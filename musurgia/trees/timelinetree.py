from typing import Any
from verysimpletree.tree import Tree

from musurgia.musurgia_exceptions import WrongNodeDurationError
from musurgia.timing.duration import Duration

__all__ = ["TimeLineNodeContainer", "TimelineTree"]

class TimeLineNodeContainer:
    def __init__(self, timeline_node: "TimelineTree", duration: Duration, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._timeline_node = timeline_node
        self._duration: Duration
        self.duration = duration

    @property
    def duration(self) -> Duration:
        return self._duration
    
    @duration.setter
    def duration(self, val: Duration) -> None:
        self._duration = val

    @property
    def timeline_node(self):
        return self._timeline_node


class TimelineTree(Tree[Any]):
    def __init__(self, duration: Duration, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = TimeLineNodeContainer(self, duration)

    
    # private methods
    def _check_child_to_be_added(self, child: 'TimelineTree') -> bool:
        if not isinstance(child, TimelineTree):
            raise TypeError(f'Wrong child type. Child must be of type FractalTree not {type(child)}')
        return True


    def check_timeline_durations(self):
        for ch in self.traverse():
            if not ch.is_leaf:
                if sum([gch.get_duration() for gch in ch.get_children()]) != ch.get_duration():
                    raise WrongNodeDurationError(f"Children of TimelineTree node of position {ch.get_position_in_tree()} with duration {ch.get_duration().seconds} have wrong durations {[gch.get_duration().seconds for gch in ch.get_children()]} ")
        return True

    def get_duration(self):
        return self.content.duration
    
    def get_value(self):
        return float(self.content.duration.seconds)
    