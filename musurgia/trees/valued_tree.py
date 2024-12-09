from abc import abstractmethod
from verysimpletree.tree import Tree
from typing import Any


class ValuedTree(Tree[Any]):
    @abstractmethod        
    def get_value(self) -> float:
        """Each child must have a get_value() method"""