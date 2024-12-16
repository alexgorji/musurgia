from abc import abstractmethod
from fractions import Fraction
import warnings
from verysimpletree.tree import Tree
from typing import Any, TypeVar, Union
from musurgia.musurgia_exceptions import WrongTreeValueError, WrongTreeValueWarning
from musurgia.musurgia_types import ConvertibleToFraction

T = TypeVar('T', bound='ValuedTree')

class ValuedTree(Tree[Any]):
    @abstractmethod
    def _set_value(self, val: ConvertibleToFraction) -> None:
        """_set_value must be defined."""
 
    def _change_children_value(self, factor: Union[int, float, Fraction]) -> None:
        for child in self._get_children():
            child._set_value(child.get_value() * factor)
            child._change_children_value(factor)
    
    def update_value(self, new_value: ConvertibleToFraction) -> None:
        if not isinstance(new_value, Fraction):
            new_value = Fraction(new_value)
        factor = Fraction(new_value, self.get_value())
        self._set_value(new_value)
        for node in self.get_reversed_path_to_root()[1:]:
            node._set_value(sum([child.get_value() for child in node._get_children()]))

        self._change_children_value(factor)

    @abstractmethod
    def get_value(self) -> Fraction:
        """get_value must be defined."""

    def _check_tree_children_values(self, children_values):
        if sum(children_values) != self.get_value():
            raise WrongTreeValueError(f"Children of ValuedTree node of position {self.get_position_in_tree()} with value {self.get_value()} have wrong values {children_values} (sum={sum(children_values)})")

    def _check_tree_children(self):
        _children = super().get_children()
        self._check_tree_children_values([ch.get_value() for ch in _children])

    def check_tree_values(self) -> bool:
        for node in self.traverse():
            if not node.is_leaf:
                node._check_tree_children()
        return True
    
    def _get_children(self: T) -> list[T]:
        return super().get_children()
    
    def get_children(self: T) -> list[T]:
        children = self._get_children()
        if not self.is_leaf:
            try:
                self._check_tree_children_values([ch.get_value() for ch in children])
            except WrongTreeValueError as err:
                warnings.warn(str(err), WrongTreeValueWarning)
        return children

    @property
    def value(self):
        raise AttributeError("Use get_value() instead.")