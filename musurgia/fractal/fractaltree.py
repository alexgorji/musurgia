from typing import Union, Optional, List, TypeVar, Callable, NewType, Literal, Any, Tuple

from fractions import Fraction
from verysimpletree.tree import Tree, NodeReturnValue

from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.permutation.permutation import LimitedPermutation, permute

NonNegativeInt = NewType('NonNegativeInt', int)
ReadingDirection = Literal['horizontal', 'vertical', 'diagonal', 'half-diagonal']

_TREE_TYPE = TypeVar('_TREE_TYPE', bound='FractalTree')
GenerateChildrenMode = Literal['reduce', 'reduce_backwards', 'reduce_forwards', 'reduce_sieve', 'merge']


def check_non_negative_int(value: int) -> NonNegativeInt:
    if value < 0:
        raise ValueError(f"NonNegativeInt value must be non-negative, got {value}")
    return NonNegativeInt(value)


class FractalTreeException(Exception):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)


class FractalTree(Tree):
    """
    FractalTree represents the node of a fractal tree with a mechanism of limited permutations.


    >>> try:
    ...     FractalTree()
    ... except TypeError as err:
    ...     assert "__init__() missing 3 required positional arguments: 'value', 'proportions', and 'main_permutation_order'" in str(err)
    >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
    >>> ft.get_value()
    Fraction(10, 1)
    >>> ft.proportions
    [Fraction(1, 6), Fraction(1, 3), Fraction(1, 2)]
    >>> ft.main_permutation_order
    (3, 1, 2)
    >>> ft.first_index
    (1, 1)
    >>> ft.reading_direction
    'horizontal'
    """

    def __init__(self, value: int,
                 proportions: Union[
                     list[int], list[float], List['Fraction'], tuple[int, ...], tuple[float, ...], Tuple[
                         'Fraction', ...]],
                 main_permutation_order: tuple[int, ...], first_index: tuple[int, int] = (1, 1),
                 reading_direction: ReadingDirection = 'horizontal', fertile: bool = True,
                 *args: Any,
                 **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._limited_permutation = None
        self._value = None
        self._proportions = None
        self._main_permutation_order = None
        self._first_index = None
        self._reading_direction = reading_direction
        self._fertile = None
        self._fractal_order = None
        self._children_fractal_values = None
        self._permutation_order = None
        self._set_value(value)
        self.proportions = proportions
        self.main_permutation_order = main_permutation_order
        self.first_index = first_index
        self.reading_direction = reading_direction
        self.fertile = fertile

    # private methods

    def _check_child_to_be_added(self, child: '_TREE_TYPE') -> bool:
        if isinstance(child, FractalTree):
            return True
        else:
            return False

    def _calculate_children_fractal_values(self) -> List['Fraction']:
        if self.is_root:
            permute([self.get_value() * prop for prop in self.proportions], self.main_permutation_order)
        return permute([self.get_value() * prop for prop in self.proportions], self.get_permutation_order())

    def _change_children_value(self, factor: Union[int, float, Fraction]) -> None:
        for child in self.get_children():
            child._value *= factor
            child._change_children_value(factor)

    def _get_child_first_index(self, parent: '_TREE_TYPE', index: int) -> tuple[int, int]:
        if self.is_root:
            first_index_x = parent.first_index[0]
        else:
            first_index_x = sum(parent.first_index) % self.get_size()

        if first_index_x == 0:
            first_index_x = self.get_size()
        return first_index_x, index + 1

    def _set_permutation_order(self) -> None:
        if self.main_permutation_order and self.first_index and self.reading_direction:
            self._limited_permutation = LimitedPermutation(input_list=list(range(1, self.get_size() + 1)),
                                                           main_permutation_order=self.main_permutation_order,
                                                           first_index=self.first_index,
                                                           reading_direction=self.reading_direction)  # type: ignore
            self._permutation_order = self._limited_permutation.get_permutation_order_iterator().__next__()  # type: ignore

    def _set_value(self, val: Union[int, float, Fraction]) -> None:
        if not isinstance(val, Fraction):
            val = Fraction(val)
        self._value = val

    # properties
    @property
    def fertile(self) -> bool:
        return self._fertile  # type: ignore

    @fertile.setter
    def fertile(self, val: bool) -> None:
        self._fertile = val

    @property
    def first_index(self) -> tuple[int, int]:
        return self._first_index  # type: ignore

    @first_index.setter
    def first_index(self, value: tuple[int, int]) -> None:
        self._first_index = value
        self._set_permutation_order()

    @property
    def proportions(self) -> List['Fraction']:
        return self._proportions  # type: ignore

    @proportions.setter
    def proportions(self, values: Union[
        List[int], List[float], List['Fraction'], Tuple[int], Tuple[float], Tuple['Fraction']]) -> None:
        self._proportions = [Fraction(Fraction(value) / Fraction(sum(values))) for value in values]

    @property
    def main_permutation_order(self) -> tuple[int]:
        return self._main_permutation_order  # type: ignore

    @main_permutation_order.setter
    def main_permutation_order(self, value: tuple[int]) -> None:
        self._main_permutation_order = value
        self._set_permutation_order()

    @property
    def reading_direction(self) -> ReadingDirection:
        return self._reading_direction

    @reading_direction.setter
    def reading_direction(self, value: ReadingDirection) -> None:
        self._reading_direction = value
        self._set_permutation_order()

    def add_layer(self, *conditions: Optional[Callable[['_TREE_TYPE'], bool]]) -> None:
        """
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.add_layer()
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [3, 1, 2]
        >>> ft.get_leaves(key=lambda leaf: leaf.first_index)
        [(1, 1), (1, 2), (1, 3)]
        >>> ft.get_leaves(key=lambda leaf: round(float(leaf.get_value() ), 2))
        [5.0, 1.67, 3.33]
        >>> ft.add_layer()
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [[3, 1, 2], [2, 3, 1], [1, 2, 3]]
        >>> ft.get_leaves(key=lambda leaf: round(float(leaf.get_value() ), 2))
        [[2.5, 0.83, 1.67], [0.56, 0.83, 0.28], [0.56, 1.11, 1.67]]


        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.add_layer()
        >>> ft.get_children()[0].add_layer()
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [[3, 1, 2], 1, 2]
        >>> ft.get_leaves(key=lambda leaf: round(float(leaf.get_value() ), 2))
        [[2.5, 0.83, 1.67], 1.67, 3.33]
        """

        leaves = list(self.iterate_leaves())
        if not leaves:
            leaves = [self]

        if conditions is not None:
            for leaf in leaves:
                for condition in conditions:
                    if condition(leaf) is False:
                        leaf.fertile = False
                        break

        for leaf in leaves:
            if leaf.fertile is True:
                for i in range(leaf.get_size()):
                    new_node = leaf.__copy__()
                    new_node._value = leaf.get_children_fractal_values()[i]
                    new_node.first_index = self._get_child_first_index(leaf, i)
                    leaf.add_child(new_node)
                    new_node._fractal_order = leaf.get_children_fractal_orders()[i]

            else:
                pass

    def change_value(self, new_value: Union[int, float, Fraction]) -> None:
        """
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.change_value(20)
        >>> ft.get_value()
        Fraction(20, 1)
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.add_layer()
        >>> ft.get_children()[0].change_value(10)
        >>> ft.get_value()
        Fraction(15, 1)
        >>> [child.get_value() for child in ft.get_children()]
        [Fraction(10, 1), Fraction(5, 3), Fraction(10, 3)]
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.add_layer()
        >>> ft.change_value(15)
        >>> [child.get_value() for child in ft.get_children()]
        [Fraction(15, 2), Fraction(5, 2), Fraction(5, 1)]
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.add_layer()
        >>> ft.add_layer()
        >>> ft.get_children()[0].change_value(10)
        >>> print(ft.get_tree_representation(key=lambda node: node.get_value()))
        └── 15
            ├── 10
            │   ├── 5
            │   ├── 5/3
            │   └── 10/3
            ├── 5/3
            │   ├── 5/9
            │   ├── 5/6
            │   └── 5/18
            └── 10/3
                ├── 5/9
                ├── 10/9
                └── 5/3
        <BLANKLINE>
        """
        factor = Fraction(new_value, self.get_value())  # type: ignore
        self._set_value(new_value)
        for node in self.get_reversed_path_to_root()[1:]:
            node._value = sum([child.get_value() for child in node.get_children()])

        self._change_children_value(factor)

    def get_value(self) -> int:
        return self._value  # type: ignore

    def get_children_fractal_values(self) -> List['Fraction']:
        """
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.add_layer()
        >>> ft.get_children_fractal_values()
        [Fraction(5, 1), Fraction(5, 3), Fraction(10, 3)]
        """
        if not self._children_fractal_values:
            self._children_fractal_values = self._calculate_children_fractal_values()
        return self._children_fractal_values  # type: ignore

    def get_children_fractal_orders(self) -> list[int]:
        if self.is_root:
            return permute(list(range(1, self.get_size() + 1)), self.main_permutation_order)
        return permute(list(range(1, self.get_size() + 1)), self.get_permutation_order())

    def get_fractal_order(self) -> int:
        """
        :return:

        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.add_layer()
        >>> [node.get_fractal_order() for node in ft.traverse()]
        [None, 3, 1, 2]
        """
        return self._fractal_order  # type: ignore

    def get_layer(self, layer: int, key: Optional[Union[str, Callable[[_TREE_TYPE], Any]]] = None) -> List[
        '_TREE_TYPE']:
        """
        :param layer:
        :param key:
        :return:

        >>> ft = FractalTree(10, (1, 2, 3), (3, 1, 2))
        >>> ft.add_layer()
        >>> for i in range(3):
        ...     ft.add_layer(lambda n: True if n.get_fractal_order() > 1 else False)
        >>> print(ft.get_layer(0, key=lambda node: node.get_fractal_order()))
        None
        >>> ft.get_layer(1, key=lambda node: node.get_fractal_order())
        [3, 1, 2]
        >>> ft.get_layer(2, key=lambda node: node.get_fractal_order())
        [[3, 1, 2], 1, [1, 2, 3]]
        >>> ft.get_layer(3, key=lambda node: node.get_fractal_order())
        [[[3, 1, 2], 1, [1, 2, 3]], 1, [1, [2, 3, 1], [1, 2, 3]]]
        >>> ft.get_layer(4, key=lambda node: node.get_fractal_order())
        [[[[3, 1, 2], 1, [1, 2, 3]], 1, [1, [2, 3, 1], [1, 2, 3]]], 1, [1, [[3, 1, 2], [2, 3, 1], 1], [1, [2, 3, 1], [1, 2, 3]]]]
        """
        if layer > self.get_root().get_number_of_layers():
            raise ValueError(f'FractalTree.get_layer: max layer number={self.get_number_of_layers()}')
        else:
            if layer == 0:
                return NodeReturnValue(self, key).get_return_value()
            else:
                if self.is_leaf:
                    return self.get_layer(layer=layer - 1, key=key)
                output = []
                for child in self.get_children():
                    if child.get_farthest_leaf().get_distance() == 1:
                        output.append(NodeReturnValue(child, key).get_return_value())
                    else:
                        output.append(child.get_layer(layer - 1, key))
                return output

    def get_limited_permutation_object(self) -> LimitedPermutation:
        return self._limited_permutation  # type: ignore

    def get_number_of_layers(self) -> int:
        if self.get_leaves() == [self]:
            return 0
        else:
            return self.get_farthest_leaf().get_distance(self)

    def get_permutation_order(self) -> Tuple[int]:
        return self._permutation_order  # type: ignore

    def get_size(self) -> int:
        """
        >>> ft = FractalTree(10, (1, 2, 3), (3, 1, 2))
        >>> ft.get_size()
        3
        """
        return len(self.proportions)

    def generate_children(self, number_of_children: Union[int, tuple], mode: GenerateChildrenMode = 'reduce',
                          merge_index: int = 0) -> None:
        """
        :param number_of_children:
        :param mode:
        :param merge_index:

        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.generate_children(number_of_children=((1, 3), 2, (1, (1, 3), 3)))
        >>> print(ft.get_tree_representation(key=lambda node: str(node.get_fractal_order())))
        └── None
            ├── 3
            │   ├── 3
            │   │   ├── 1
            │   │   ├── 2
            │   │   └── 3
            │   ├── 1
            │   │   └── 3
            │   └── 2
            │       ├── 2
            │       │   └── 3
            │       └── 3
            │           ├── 3
            │           ├── 1
            │           └── 2
            ├── 1
            │   ├── 2
            │   │   └── 3
            │   └── 3
            │       ├── 1
            │       ├── 2
            │       └── 3
            └── 2
                ├── 2
                └── 3
        <BLANKLINE>
        """

        if self.get_children():
            raise ValueError(
                f'FractalTree.generate_children: node has already children: {[ch.get_value() for ch in self.get_children()]}')

        permitted_modes = ['reduce', 'reduce_backwards', 'reduce_forwards', 'reduce_sieve', 'merge']
        if mode not in permitted_modes:
            raise ValueError(f'generate_children.mode {mode} must be in {permitted_modes}')

        if isinstance(number_of_children, int):
            if number_of_children > self.get_size():
                raise ValueError(
                    f'generate_children.number_of_children {number_of_children} can not be a greater than size {self.get_size()}')
            if number_of_children < 0:
                raise ValueError(
                    'generate_children.number_of_children {} must be a positive int'.format(number_of_children))
            elif number_of_children == 0:
                pass
            else:
                self.add_layer()
                if mode in ['reduce', 'reduce_backwards']:
                    self.reduce_children(
                        lambda child: child.get_fractal_order() < self.get_size() - number_of_children + 1)
                elif mode == 'reduce_forwards':
                    self.reduce_children(
                        lambda child: child.get_fractal_order() > number_of_children)
                elif mode == 'reduce_sieve':
                    if number_of_children == 1:
                        self.reduce_children(condition=lambda child: child.get_fractal_order() not in [1])
                    else:
                        ap = ArithmeticProgression(a1=1, an=self.get_size(), n=number_of_children)
                        selection = [int(round(x)) for x in ap]
                        self.reduce_children(condition=lambda child: child.get_fractal_order() not in selection)
                else:
                    merge_lengths = self._get_merge_lengths(number_of_children, merge_index)
                    self.merge_children(*merge_lengths)

        elif isinstance(number_of_children, tuple):
            self.generate_children(len(number_of_children), mode=mode, merge_index=merge_index)

            for index, child in enumerate(self.get_children()):
                if mode == 'reduce':
                    number_of_grand_children = number_of_children[
                        child.get_fractal_order() - child.get_size() + len(number_of_children) - 1]
                else:
                    number_of_grand_children = number_of_children[index]
                child.generate_children(number_of_grand_children, mode=mode, merge_index=merge_index)

        else:
            raise TypeError('generate_children.number_of_children must be of type int or tuple')

    def reduce_children(self, condition: Callable[['_TREE_TYPE'], bool]) -> None:
        if not self.get_children():
            raise ValueError(f'{self} has no children to be reduced')
        to_be_removed = [child for child in self.get_children() if condition(child)]
        for child in to_be_removed:
            child.up._children.remove(child)
            del child
        reduced_value = sum([child.get_value() for child in self.get_children()])
        factor = self.get_value() / reduced_value
        for child in self.get_children():
            new_value = child.get_value() * factor
            child.change_value(new_value)

        self._children_fractal_values = [child.get_value() for child in self.get_children()]

    # copy
    def __copy__(self: '_TREE_TYPE') -> '_TREE_TYPE':
        """
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), reading_direction='vertical')
        >>> ft.add_layer()
        >>> ft.add_layer()
        >>> node = ft.get_children()[1]
        >>> copied_node = node.__copy__()
        >>> for n, cp in zip(node.traverse(), copied_node.traverse()):
        ...    if n == cp:
        ...        raise Exception('n == cp')
        ...    if n.get_value() != cp.get_value():
        ...        raise Exception('n.get_value() != cp.get_value()')
        ...    for attr in ['proportions', 'main_permutation_order', 'reading_direction', 'fertile']:
        ...        if getattr(node, attr) != getattr(copied_node, attr):
        ...            raise Exception(f'n.{attr} != cp.{attr}')
        >>> copied_node.is_root, copied_node.is_leaf
        (True, True)
        """

        return self.__class__(value=self.get_value(), proportions=self.proportions,
                              main_permutation_order=self.main_permutation_order, fertile=self.fertile)
