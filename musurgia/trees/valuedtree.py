from abc import abstractmethod
from fractions import Fraction
from verysimpletree.tree import Tree
from typing import Any, Union
from musurgia.musurgia_exceptions import WrongTreeValueError
from musurgia.musurgia_types import ConvertibleToFraction

class ValuedTree(Tree[Any]):
    @abstractmethod
    def _set_value(self, val: ConvertibleToFraction) -> None:
        """_set_value must be defined."""
 
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

    def check_tree_values(self) -> bool:
        for ch in self.traverse():
            if not ch.is_leaf:
                children_values = [gch.get_value() for gch in ch.get_children()]
                if sum([gch.get_value() for gch in ch.get_children()]) != ch.get_value():
                    raise WrongTreeValueError(f"Children of ValuedTree node of position {ch.get_position_in_tree()} with value {ch.get_value()} have wrong values {children_values} (sume={sum(children_values)})")
        return True