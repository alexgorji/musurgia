from abc import abstractmethod
from fractions import Fraction
from verysimpletree.tree import Tree
from typing import Any, Union
from musurgia.musurgia_types import ConvertibleToFraction

class ValuedTree(Tree[Any]):
    # def __init__(self, value: ConvertibleToFraction, *args: Any, **kwargs: Any):
    #     super().__init__(*args, **kwargs)
    #     self._value: Fraction
    #     self._set_value(value)

    @abstractmethod
    def _set_value(self, val: ConvertibleToFraction) -> None:
        """_set_value must be defined."""
        # if not isinstance(val, Fraction):
        #     val = Fraction(val)
        # self._value = val
 
    def _change_children_value(self, factor: Union[int, float, Fraction]) -> None:
        for child in self.get_children():
            child._set_value(child.get_value() * factor)
            child._change_children_value(factor)
    
    def change_value(self, new_value: ConvertibleToFraction) -> None:
        factor = Fraction(Fraction(new_value), self.get_value())
        self._set_value(new_value)
        for node in self.get_reversed_path_to_root()[1:]:
            node._set_value(sum([child.get_value() for child in node.get_children()]))

        self._change_children_value(factor)

    @abstractmethod
    def get_value(self) -> Fraction:
        """get_value must be defined."""
    # def get_value(self) -> Fraction:
    #     return self._value


