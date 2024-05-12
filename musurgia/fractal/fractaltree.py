from pprint import pprint
from typing import Union

from quicktions import Fraction
from tree.tree import Tree

from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.permutation.permutation import LimitedPermutation, permute


class FractalTreeException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class FractalTree(Tree):
    """
    FractalTree represents the node of a fractal tree with a mechanism of limited permutations.


    >>> try:
    ...     FractalTree()
    ... except TypeError as err:
    ...     assert "__init__() missing 3 required positional arguments: 'value', 'proportions', and 'main_permutation_order'" in str(err)
    >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
    >>> ft.value
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

    def __init__(self, value: int, proportions: Union[list, tuple], main_permutation_order: tuple, first_index=(1, 1),
                 reading_direction='horizontal', fertile: bool = True,
                 *args,
                 **kwargs):
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
        self.value = value
        self.proportions = proportions
        self.main_permutation_order = main_permutation_order
        self.first_index = first_index
        self.reading_direction = reading_direction
        self.fertile = fertile

    def _set_permutation_order(self):
        if self.main_permutation_order and self.first_index and self.reading_direction:
            lp = LimitedPermutation(input_list=list(range(1, self.get_size() + 1)),
                                    main_permutation_order=self.main_permutation_order, first_index=self.first_index,
                                    reading_direction=self.reading_direction)
            self._limited_permutation = lp
            self._permutation_order = lp.get_permutation_order_iterator().__next__()

    # private methods

    def _check_child_to_be_added(self, child):
        if isinstance(child, FractalTree):
            return True
        else:
            return False

    def _calculate_children_fractal_values(self):
        if self.is_root:
            permute([self.value * prop for prop in self.proportions], self.main_permutation_order)
        return permute([self.value * prop for prop in self.proportions], self.get_permutation_order())

    def _change_children_value(self, factor):
        for child in self.get_children():
            child._value *= factor
            child._change_children_value(factor)

    def get_branch(self):
        output = [self]
        node = self
        while node.up is not None:
            output.append(node.up)
            node = node.up
        output.reverse()
        return output

    def _get_child_first_index(self, parent, index):
        if self.is_root:
            first_index_x = parent.first_index[0]
        else:
            first_index_x = sum(parent.first_index) % self.get_size()

        if first_index_x == 0:
            first_index_x = self.get_size()
        return first_index_x, index + 1

    # properties
    @property
    def fertile(self):
        """
        :return:

        >>> FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), fertile='True')
        Traceback (most recent call last):
            ...
        TypeError: fertile.value must be of type bool
        """
        return self._fertile

    @fertile.setter
    def fertile(self, val):
        if not isinstance(val, bool):
            raise TypeError('fertile.value must be of type bool')
        self._fertile = val

    @property
    def first_index(self):
        return self._first_index

    @first_index.setter
    def first_index(self, value):
        self._first_index = value
        self._set_permutation_order()

    @property
    def proportions(self):
        return self._proportions

    @proportions.setter
    def proportions(self, values):
        """
        >>> FractalTree(value=10, proportions='(1, 2, 3)', main_permutation_order=(3, 1, 2))
        Traceback (most recent call last):
            ...
        TypeError: proportions must be of type list or tuple
        >>> FractalTree(value=10, proportions=1, main_permutation_order=(3, 1, 2))
        Traceback (most recent call last):
            ...
        TypeError: proportions must be of type list or tuple
        >>> FractalTree(value=10, main_permutation_order=(3, 1, 2), proportions=(1, 2))
        Traceback (most recent call last):
            ...
        ValueError: _permutation_order must have the same length as the proportions
        """

        self._proportions = [Fraction(Fraction(value) / Fraction(sum(values))) for value in values]

    @property
    def main_permutation_order(self):
        return self._main_permutation_order

    @main_permutation_order.setter
    def main_permutation_order(self, value):
        self._main_permutation_order = value
        self._set_permutation_order()

    @property
    def reading_direction(self):
        return self._reading_direction

    @reading_direction.setter
    def reading_direction(self, value):
        self._reading_direction = value
        self._set_permutation_order()

    @property
    def value(self):
        """
        >>> ft = FractalTree(value='10', proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.value
        Fraction(10, 1)

        :return:
        """
        return self._value

    @value.setter
    def value(self, val):
        if not isinstance(val, Fraction):
            val = Fraction(val)
        self._value = val

    def add_layer(self, *conditions):
        """
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.add_layer()
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [3, 1, 2]
        >>> ft.get_leaves(key=lambda leaf: leaf.first_index)
        [(1, 1), (1, 2), (1, 3)]
        >>> ft.get_leaves(key=lambda leaf: round(float(leaf.value), 2))
        [5.0, 1.67, 3.33]
        >>> ft.add_layer()
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [[3, 1, 2], [2, 3, 1], [1, 2, 3]]
        >>> ft.get_leaves(key=lambda leaf: round(float(leaf.value), 2))
        [[2.5, 0.83, 1.67], [0.56, 0.83, 0.28], [0.56, 1.11, 1.67]]


        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.add_layer()
        >>> ft.get_children()[0].add_layer()
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [[3, 1, 2], 1, 2]
        >>> ft.get_leaves(key=lambda leaf: round(float(leaf.value), 2))
        [[2.5, 0.83, 1.67], 1.67, 3.33]
        """

        leaves = list(self.iterate_leaves())
        if not leaves:
            leaves = [self]

        if conditions:
            for leaf in leaves:
                for condition in conditions:
                    if not condition(leaf):
                        leaf.fertile = False
                        break

        for leaf in leaves:
            if leaf.fertile is True:
                for i in range(leaf.get_size()):
                    new_node = leaf.__copy__()
                    new_node.value = leaf.get_children_fractal_values()[i]
                    # if self.is_root:
                    #     new_node.first_index = self.first_index
                    # else:
                    new_node.first_index = self._get_child_first_index(leaf, i)
                    leaf.add_child(new_node)
                    new_node._fractal_order = leaf.get_children_fractal_orders()[i]

            else:
                pass

    def change_value(self, new_value):
        factor = Fraction(new_value, self.value)
        self._value = new_value
        for node in reversed(self.get_branch()[:-1]):
            node._value = sum([child.value for child in node.get_children()])

        self._change_children_value(factor)

    def get_fractal_order(self):
        return self._fractal_order

    def get_children_fractal_values(self):
        if not self._children_fractal_values:
            self._children_fractal_values = self._calculate_children_fractal_values()
        return self._children_fractal_values

    def get_children_fractal_orders(self):
        if self.is_root:
            return permute(list(range(1, self.get_size() + 1)), self.main_permutation_order)
        return permute(list(range(1, self.get_size() + 1)), self.get_permutation_order())

    def generate_children(self, number_of_children, mode='reduce', merge_index=0) -> list['FractalTree']:
        """

        :param number_of_children:
        :param mode:
        :param merge_index:
        :return:

        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.generate_children(number_of_children=3, mode='wrong')
        Traceback (most recent call last):
            ...
        ValueError: generate_children.mode wrong must be in ['reduce', 'reduce_backwards', 'reduce_forwards', 'reduce_sieve', 'merge']

        >>> ft.generate_children(number_of_children="1")
        Traceback (most recent call last):
            ...
        TypeError: generate_children.number_of_children must be of type int or tuple

        >>> ft.generate_children(number_of_children=4)
        Traceback (most recent call last):
            ...
        ValueError: generate_children.number_of_children 4 can not be a greater than size 3

        >>> ft.generate_children(number_of_children=-1)
        Traceback (most recent call last):
            ...
        ValueError: generate_children.number_of_children -1 must be a positive int

        >>> ft.generate_children(number_of_children=0)
        [None]

        >>> ft.generate_children(3)
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [3, 1, 2]

        >>> ft.generate_children(number_of_children=1)
        Traceback (most recent call last):
            ...
        ValueError: FractalTree.generate_children: node has already children: [Fraction(5, 1), Fraction(5, 3), Fraction(10, 3)]


        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.generate_children(number_of_children=1)
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [3]

        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.generate_children(number_of_children=2)
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [3, 2]

        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.generate_children(number_of_children=3)
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [3, 1, 2]


        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.generate_children(number_of_children=(3, 3, 3))
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [[3, 1, 2], [2, 3, 1], [1, 2, 3]]

        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.generate_children(number_of_children=(2, 2, 2))
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [[3, 2], [2, 3], [2, 3]]

        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.generate_children(number_of_children=(1, 1, 1))
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [[3], [3], [3]]

        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> pprint(ft.get_limited_permutation_object().get_permutation_orders())
        [[(3, 1, 2), (2, 3, 1), (1, 2, 3)],
         [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
         [(2, 3, 1), (1, 2, 3), (3, 1, 2)]]
        >>> ft.generate_children(number_of_children=(1, 2, 3))
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [[3, 1, 2], [3], [2, 3]]

        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.generate_children(number_of_children=(0, 1, 2))
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [[3, 2], 1, [3]]

        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.generate_children(number_of_children=(1, (1, 2, 3), 3))
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [[3, 1, 2], [3], [[3], [2, 3], [1, 2, 3]]]

        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2))
        >>> ft.generate_children(number_of_children=((1, 3), 2, (1, (1, 3), 3)))
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [[[1, 2, 3], [3], [[3], [3, 1, 2]]], [[3], [1, 2, 3]], [2, 3]]
        """

        if self.get_children():
            raise ValueError(
                f'FractalTree.generate_children: node has already children: {[ch.value for ch in self.get_children()]}')

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
                return [None]
            else:
                self.add_layer()
                if mode in ['reduce', 'reduce_backwards']:
                    self.reduce_children(
                        lambda child: child.get_fractal_order() < self.get_size() - number_of_children + 1)
                elif mode == 'reduce_forwards':
                    self.reduce_children(
                        lambda child: child.fractal_order > number_of_children)
                elif mode == 'reduce_sieve':
                    if number_of_children == 1:
                        self.reduce_children(condition=lambda child: child.fractal_order not in [1])
                    else:
                        ap = ArithmeticProgression(a1=1, an=self.get_size(), n=number_of_children)
                        selection = [int(round(x)) for x in ap]
                        self.reduce_children(condition=lambda child: child.fractal_order not in selection)
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

    def get_limited_permutation_object(self):
        return self._limited_permutation

    def get_permutation_order(self):
        return self._permutation_order

    def get_size(self):
        """
        >>> ft = FractalTree(10, (1, 2, 3), (3, 1, 2))
        >>> ft.get_size()
        3

        :return:
        """
        return len(self.proportions)

    def reduce_children(self, condition):
        """

        :param condition:
        :return:



        """
        if not self.get_children():
            raise ValueError(f'{self} has no children to be reduced')
        to_be_removed = [child for child in self.get_children() if condition(child)]
        for child in to_be_removed:
            child.up._children.remove(child)
            del child
        reduced_value = sum([child.value for child in self.get_children()])
        factor = self.value / reduced_value
        for child in self.get_children():
            new_value = child.value * factor
            child.change_value(new_value)

        self._children_fractal_values = [child.value for child in self.get_children()]

    # copy
    def __copy__(self):
        return self.__class__(value=self.value, proportions=self.proportions,
                              main_permutation_order=self.main_permutation_order, fertile=self.fertile)
