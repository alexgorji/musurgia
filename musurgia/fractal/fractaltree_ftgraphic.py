import copy
import itertools
from fractions import Fraction
from typing import Union, Optional, List, Callable, Any, cast, Sequence

from verysimpletree.tree import Tree

from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.matrix.matrix import PermutationOrderMatrix, PermutationOrderMatrixGenerator
from musurgia.musurgia_exceptions import FractalTreeHasChildrenError, \
    FractalTreeNonRootCannotSetMainPermutationOrderError, PermutationIndexCalculaterNoParentIndexError, \
    FractalTreePermutationIndexError, FractalTreeSetMainPermutationOrderFirstError
from musurgia.musurgia_types import ConvertibleToFraction, FractalTreeReduceChildrenMode, convert_to_fraction, \
    MatrixIndex, PermutationOrder, check_type, PositiveInteger, check_matrix_index_values, create_error_message, \
    ConvertibleToFloat
from musurgia.pdf.drawobject import DrawObject
from musurgia.pdf.labeled import Labeled
from musurgia.pdf.line import HorizontalLineSegment, HorizontalSegmentedLine
from musurgia.pdf.margined import Margined
from musurgia.pdf.positioned import Positioned
from musurgia.pdf.rowcolumn import DrawObjectColumn, DrawObjectRow
from musurgia.permutation.permutation import permute
from musurgia.tests.utils_for_tests import node_info
from musurgia.utils import flatten

__all__ = ['FractalTree', 'FractalTreeNodeSegment']


class PermutationIndexCalculater:
    def __init__(self, size: PositiveInteger, parent_index: Optional[MatrixIndex] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._size: PositiveInteger
        self._parent_index: Optional[MatrixIndex] = None

        self.size = size
        self.parent_index = parent_index

    @property
    def size(self) -> PositiveInteger:
        return self._size

    @size.setter
    def size(self, value: PositiveInteger) -> None:
        check_type(value, 'PositiveInteger', class_name=self.__class__.__name__, property_name='size')
        self._size = value

    @property
    def parent_index(self) -> Optional[MatrixIndex]:
        return self._parent_index

    @parent_index.setter
    def parent_index(self, value: MatrixIndex) -> None:
        if value is not None:
            check_type(value, 'MatrixIndex', class_name=self.__class__.__name__, property_name='parent_index')
        self._parent_index = value

    def get_index(self, column_number: PositiveInteger) -> MatrixIndex:
        if self.parent_index is None:
            raise PermutationIndexCalculaterNoParentIndexError
        check_type(column_number, 'PositiveInteger', class_name=self.__class__.__name__, method_name='get_index',
                   argument_name='column_number')
        if column_number > self.size:
            raise ValueError(f'Column number {column_number} cannot be less than size {self.size}')
        r = sum(self.parent_index) % self.size
        if r == 0:
            r = self.size
        return r, column_number


class FractalTreeNodeSegment(HorizontalLineSegment):
    def __init__(self, node_value, unit=1, *args, **kwargs):
        super().__init__(length=node_value * unit, *args, **kwargs)
        self._node_value = node_value
        self._unit: int
        self.unit = unit

    def _update_length(self):
        self.straight_line.length = self.get_node_value() * self.unit

    @property
    def length(self) -> float:
        return super().length

    @property
    def unit(self) -> int:
        return self._unit

    @unit.setter
    def unit(self, value: int) -> None:
        self._unit = value
        self._update_length()

    def get_node_value(self):
        return self._node_value

    def set_node_value(self, val):
        self._node_value = val
        self._update_length()


class FractalTree(Tree[Any]):
    """
    FractalTree represents the node of a fractal tree with a mechanism of limited permutations.
    """

    def __init__(self, value: ConvertibleToFraction,
                 proportions: Sequence[ConvertibleToFraction],
                 main_permutation_order: Optional[PermutationOrder] = None,
                 permutation_index: Optional[MatrixIndex] = None,
                 fertile: bool = True,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self._permutation_order_matrix: Optional[PermutationOrderMatrix]
        self._value: Fraction
        self._proportions: Sequence[ConvertibleToFraction] = []
        self._main_permutation_order: Optional[PermutationOrder] = None
        self._permutation_index: Optional[MatrixIndex] = None
        self._fertile: bool

        self._fractal_order: int
        self._children_fractal_values = None
        self._children_permutation_order_matrices = None
        self._permutation_order = None
        self._node_segment: FractalTreeNodeSegment
        self._set_value(value)

        self.proportions = proportions
        self.main_permutation_order = main_permutation_order
        self.set_permutation_index(permutation_index)
        self.fertile = fertile

        self._pic = None

        # self._graphic = _Graphic(self)

    # private methods

    def _check_child_to_be_added(self, child: 'FractalTree') -> bool:
        if isinstance(child, FractalTree):
            if child._main_permutation_order is not None:
                raise FractalTreeNonRootCannotSetMainPermutationOrderError
            return True
        else:
            return False

    def _calculate_children_fractal_values(self) -> list['Fraction']:
        return permute([self.get_value() * prop for prop in self.proportions], self.get_permutation_order())

    def _change_children_value(self, factor: Union[int, float, Fraction]) -> None:
        for child in self.get_children():
            child._set_value(child._value * factor)
            child._change_children_value(factor)

    def _get_children_fractal_values(self) -> List['Fraction']:
        """
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        >>> ft.add_layer()
        >>> ft._get_children_fractal_values()
        [Fraction(5, 1), Fraction(5, 3), Fraction(10, 3)]
        """
        if not self._children_fractal_values:
            self._children_fractal_values = self._calculate_children_fractal_values()
        return self._children_fractal_values

    def _get_merge_lengths(self, size, merge_index):
        if size == 1:
            return [self.get_size()]

        lengths = self.get_size() * [1]
        pointer = merge_index
        sliced_lengths = [lengths[:pointer], lengths[pointer:]]

        if not sliced_lengths[0]:
            sliced_lengths = sliced_lengths[1:]

        while len(sliced_lengths) < size and len(sliced_lengths[0]) > 1:
            temp = sliced_lengths[0]
            sliced_lengths[0] = temp[:-1]
            sliced_lengths.insert(1, temp[-1:])

        while len(sliced_lengths) < size and len(sliced_lengths[pointer]) > 1:
            temp = sliced_lengths[pointer]
            sliced_lengths[pointer] = temp[:-1]
            sliced_lengths.insert(pointer + 1, temp[-1:])

        sliced_lengths = [len(x) for x in sliced_lengths]

        return sliced_lengths

    def _get_pic(self):
        if self.is_root:
            if self._pic is None:
                self._pic = PermutationIndexCalculater(self.get_permutation_order_matrix().get_size())
            return self._pic
        return self.get_root()._get_pic()

    def _set_value(self, val: ConvertibleToFraction) -> None:
        if not isinstance(val, Fraction):
            val = Fraction(val)
        self._value = val
        try:
            self.get_node_segment().set_node_value(val)
        except AttributeError:
            self._node_segment = FractalTreeNodeSegment(node_value=val)

    # properties
    @property
    def fertile(self) -> bool:
        return self._fertile

    @fertile.setter
    def fertile(self, val: bool) -> None:
        self._fertile = val

    # @property
    # def graphic(self):
    #     return self._graphic

    @property
    def main_permutation_order(self) -> Optional[PermutationOrder]:
        if self.is_root:
            return self._main_permutation_order
        else:
            return self.get_root().main_permutation_order

    @main_permutation_order.setter
    def main_permutation_order(self, value: Optional[PermutationOrder]) -> None:
        if self.get_children():
            raise FractalTreeHasChildrenError
        if value is not None:
            if not self.is_root:
                raise FractalTreeNonRootCannotSetMainPermutationOrderError
            check_type(value, 'PermutationOrder', class_name=self.__class__.__name__,
                       property_name='main_permutation_order')
            self._pic = None
            self._permutation_order_matrix = PermutationOrderMatrixGenerator(
                main_permutation_order=value).generate_permutation_order_matrix()
        else:
            self._permutation_order_matrix = None
        self._main_permutation_order = value

    @property
    def proportions(self) -> Sequence[ConvertibleToFraction]:
        return self._proportions

    @proportions.setter
    def proportions(self, values: Sequence[ConvertibleToFraction]) -> None:
        converted_values: List[Fraction] = [convert_to_fraction(val) for val in list(values)]
        total = sum(converted_values)
        self._proportions = [Fraction(value, total) for value in converted_values]

    # public methods
    def add_layer(self, *conditions: Optional[Callable[['FractalTree'], bool]]) -> None:
        """
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        >>> ft.add_layer()
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [3, 1, 2]
        >>> ft.get_leaves(key=lambda leaf: leaf.get_permutation_index())
        [(2, 1), (2, 2), (2, 3)]
        >>> ft.get_leaves(key=lambda leaf: round(float(leaf.get_value() ), 2))
        [5.0, 1.67, 3.33]
        >>> ft.add_layer()
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [[1, 2, 3], [3, 1, 2], [2, 3, 1]]
        >>> ft.get_leaves(key=lambda leaf: round(float(leaf.get_value() ), 2))
        [[0.83, 1.67, 2.5], [0.83, 0.28, 0.56], [1.11, 1.67, 0.56]]


        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        >>> ft.add_layer()
        >>> ft.get_children()[0].add_layer()
        >>> ft.get_leaves(key=lambda leaf: leaf.get_fractal_order())
        [[1, 2, 3], 1, 2]
        >>> ft.get_leaves(key=lambda leaf: round(float(leaf.get_value() ), 2))
        [[0.83, 1.67, 2.5], 1.67, 3.33]
        """

        leaves = list(self.iterate_leaves())
        if not leaves:
            leaves = [self]

        if conditions is not None:
            for leaf in leaves:
                for condition in conditions:
                    if cast(Callable, condition)(leaf) is False:
                        leaf.fertile = False
                        break

        for leaf in leaves:
            if leaf.fertile is True:
                for i in range(leaf.get_size()):
                    value = leaf._get_children_fractal_values()[i]
                    new_node = self.__class__(value=value, proportions=self.get_root().proportions,
                                              permutation_index=None)
                    leaf.add_child(new_node)
                    new_node.calculate_permutation_index()
                    new_node._fractal_order = leaf.get_children_fractal_orders()[i]
            else:
                pass

    def change_value(self, new_value: Union[int, float, Fraction]) -> None:
        """
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        >>> ft.change_value(20)
        >>> ft.get_value()
        Fraction(20, 1)
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        >>> ft.add_layer()
        >>> ft.get_children()[0].change_value(10)
        >>> ft.get_value()
        Fraction(15, 1)
        >>> [child.get_value() for child in ft.get_children()]
        [Fraction(10, 1), Fraction(5, 3), Fraction(10, 3)]
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        >>> ft.add_layer()
        >>> ft.change_value(15)
        >>> [child.get_value() for child in ft.get_children()]
        [Fraction(15, 2), Fraction(5, 2), Fraction(5, 1)]
        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        >>> ft.add_layer()
        >>> ft.add_layer()
        >>> ft.get_children()[0].change_value(10)
        >>> print(ft.get_tree_representation(key=lambda node: node.get_value()))
        └── 15
            ├── 10
            │   ├── 5/3
            │   ├── 10/3
            │   └── 5
            ├── 5/3
            │   ├── 5/6
            │   ├── 5/18
            │   └── 5/9
            └── 10/3
                ├── 10/9
                ├── 5/3
                └── 5/9
        <BLANKLINE>
        """
        factor = Fraction(Fraction(new_value), self.get_value())
        self._set_value(new_value)
        for node in self.get_reversed_path_to_root()[1:]:
            node._set_value(sum([child.get_value() for child in node.get_children()]))

        self._change_children_value(factor)

    def calculate_permutation_index(self):
        if self.is_root:
            raise FractalTreePermutationIndexError(
                f'{self.__class__.__name__}:calculate_permutation_index: Set permutation_index of root')
        pic = self._get_pic()
        pic.parent_index = self.up.get_permutation_index()
        self._permutation_index = pic.get_index(self.up.get_children().index(self) + 1)

    def generate_children(self, number_of_children: Union[int, tuple],
                          reduce_mode: FractalTreeReduceChildrenMode = 'backwards',
                          merge_index: int = 0) -> None:
        """
        :param number_of_children:
        :param mode:
        :param merge_index:

        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        >>> ft.generate_children(number_of_children=((1, 3), 2, (1, (1, 3), 3)))
        >>> print(ft.get_tree_representation(key=lambda node: str(node.get_fractal_order())))
        └── None
            ├── 3
            │   ├── 1
            │   │   └── 3
            │   ├── 2
            │   │   ├── 2
            │   │   │   └── 3
            │   │   └── 3
            │   │       ├── 2
            │   │       ├── 3
            │   │       └── 1
            │   └── 3
            │       ├── 3
            │       ├── 1
            │       └── 2
            ├── 1
            │   ├── 3
            │   │   ├── 3
            │   │   ├── 1
            │   │   └── 2
            │   └── 2
            │       └── 3
            └── 2
                ├── 2
                └── 3
        <BLANKLINE>
        """
        # check_generate_children_mode(reduce_mode)
        # this error must be moved to add_layer()
        if self.get_children():
            raise ValueError(
                f'FractalTree.generate_children: node has already children: {[ch.get_value() for ch in self.get_children()]}')

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
                self.reduce_children_by_size(size=number_of_children, mode=reduce_mode, merge_index=merge_index)

        elif isinstance(number_of_children, tuple):
            self.generate_children(len(number_of_children), reduce_mode=reduce_mode, merge_index=merge_index)

            for index, child in enumerate(self.get_children()):
                if reduce_mode == 'backwards':
                    number_of_grand_children = number_of_children[
                        child.get_fractal_order() - child.get_size() + len(number_of_children) - 1]
                else:
                    number_of_grand_children = number_of_children[index]
                child.generate_children(number_of_grand_children, reduce_mode=reduce_mode, merge_index=merge_index)

        else:
            raise TypeError('generate_children.number_of_children must be of type int or tuple')

    def get_children_fractal_orders(self) -> list[int]:
        if self.is_root:
            if self.main_permutation_order is None:
                raise AttributeError(
                    create_error_message(message='Set main_permutation_order first', class_name=self.__class__.__name__,
                                         method_name='get_children_fractal_orders'))
            else:
                return permute(list(range(1, self.get_size() + 1)), self.main_permutation_order)
        return permute(list(range(1, self.get_size() + 1)), self.get_permutation_order())

    def get_fractal_order(self) -> Optional[int]:
        """
        :return:

        >>> ft = FractalTree(value=10, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
        >>> ft.add_layer()
        >>> [node.get_fractal_order() for node in ft.traverse()]
        [None, 3, 1, 2]
        """
        try:
            return self._fractal_order
        except AttributeError:
            return None

    def get_layer(self, layer: int, key: Optional[Callable[['FractalTree'], Any]] = None) -> List[
        'FractalTree']:
        """
        :param layer:
        :param key:
        :return:

        >>> ft = FractalTree(10, (1, 2, 3), (3, 1, 2), (1, 1))
        >>> ft.add_layer()
        >>> for i in range(3):
        ...     ft.add_layer(lambda n: True if n.get_fractal_order() > 1 else False)
        >>> print(ft.get_layer(0, key=lambda node: node.get_fractal_order()))
        None
        >>> ft.get_layer(1, key=lambda node: node.get_fractal_order())
        [3, 1, 2]
        >>> ft.get_layer(2, key=lambda node: node.get_fractal_order())
        [[1, 2, 3], 1, [2, 3, 1]]
        >>> ft.get_layer(3, key=lambda node: node.get_fractal_order())
        [[1, [1, 2, 3], [3, 1, 2]], 1, [[1, 2, 3], [3, 1, 2], 1]]
        >>> ft.get_layer(4, key=lambda node: node.get_fractal_order())
        [[1, [1, [3, 1, 2], [2, 3, 1]], [[2, 3, 1], 1, [3, 1, 2]]], 1, [[1, [1, 2, 3], [3, 1, 2]], [[3, 1, 2], 1, [1, 2, 3]], 1]]
        """
        if layer > self.get_root().get_number_of_layers():
            raise ValueError(f'FractalTree.get_layer: max layer number={self.get_number_of_layers()}')
        else:
            if layer == 0:
                return self.get_self_with_key(key)
            else:
                if self.is_leaf:
                    return self.get_layer(layer=layer - 1, key=key)
                output = []
                for child in self.get_children():
                    if child.get_farthest_leaf().get_distance() == 1:
                        output.append(child.get_self_with_key(key))
                    else:
                        output.append(child.get_layer(layer - 1, key))
                return output

    def get_number_of_layers(self) -> int:
        if self.get_leaves() == [self]:
            return 0
        else:
            return self.get_farthest_leaf().get_distance(self)

    def get_permutation_index(self) -> MatrixIndex:
        if not self._permutation_index:
            self._permutation_index = self.calculate_permutation_index()
        return self._permutation_index

    def get_permutation_order(self) -> tuple[int, ...]:
        if not self._permutation_order:
            self._permutation_order = self.get_permutation_order_matrix().get_element(self.get_permutation_index())
        return self._permutation_order

    def get_permutation_order_matrix(self) -> PermutationOrderMatrix:
        if self.is_root:
            if self._permutation_order_matrix is None:
                raise FractalTreeSetMainPermutationOrderFirstError(
                    create_error_message(message=FractalTreeSetMainPermutationOrderFirstError.msg,
                                         class_name=self.__class__.__name__,
                                         method_name='get_permutation_order_matrix'))
            return self._permutation_order_matrix
        else:
            return self.get_root().get_permutation_order_matrix()

    def get_size(self) -> int:
        """
        >>> ft = FractalTree(10, (1, 2, 3), (3, 1, 2))
        >>> ft.get_size()
        3
        """
        return len(self.proportions)

    def get_value(self) -> Fraction:
        return self._value

    def get_node_segment(self):
        return self._node_segment

    def create_graphic(self, distance=5, unit=1, mark_line_length: float = 6, shrink_factor=0.7, layer_number=1,
                       layer_top_margin=0):
        gr = DrawObjectColumn()
        first_row = gr.add_draw_object(DrawObjectRow())
        segment = copy.deepcopy(self.get_node_segment())
        segment.unit = unit
        if layer_number == 1:
            segment.end_mark_line.length = segment.start_mark_line.length = mark_line_length
            segment.end_mark_line.show = True
            children_layer_top_margin = 0
        else:
            segment.end_mark_line.length = segment.start_mark_line.length = mark_line_length * shrink_factor
            children_layer_top_margin = (mark_line_length - segment.start_mark_line.length)
            if self.is_last_child:
                segment.end_mark_line.length = mark_line_length
                segment.end_mark_line.show = True
                children_layer_top_margin = 0
            if self.is_first_child:
                segment.start_mark_line.length = mark_line_length
                children_layer_top_margin = 0
        segment.bottom_margin += distance
        segment.top_margin += layer_top_margin
        first_row.add_draw_object(segment)
        if not self.is_leaf:
            second_row = gr.add_draw_object(DrawObjectRow())
            for ch in self.get_children():
                second_row.add_draw_object(
                    ch.create_graphic(distance, unit, mark_line_length * shrink_factor, shrink_factor,
                                      layer_number + 1, children_layer_top_margin))
        return gr

    def create_layer_graphic(self, layer_number, unit=1, mark_line_length: float = 6, shrink_factor=0.7):
        def get_ml_length(node):
            distance = node.get_distance(self)
            if distance == 0:
                return mark_line_length
            else:
                if node.is_first_child:
                    return get_ml_length(node.up)
                else:
                    return mark_line_length * shrink_factor / distance

        gr = DrawObjectRow()
        nodes = flatten(self.get_layer(layer_number))
        for node in nodes:
            copied_segment = copy.deepcopy(node.get_node_segment())
            copied_segment.unit = unit
            copied_segment.start_mark_line.length = get_ml_length(node)
            if node == nodes[-1]:
                copied_segment.end_mark_line.length = mark_line_length
                copied_segment.end_mark_line.show = True
            gr.add_draw_object(copied_segment)
        return gr

    def merge_children(self, *lengths):
        """

        :param lengths:
        :return:

        >>> ft = FractalTree(proportions=(1, 2, 3, 4, 5), main_permutation_order=(3, 5, 1, 2, 4), value=10, permutation_index=(1, 1))
        >>> ft.add_layer()
        >>> print(ft.get_tree_representation(node_info))
        └── None: (1, 1): 10.0
            ├── 3: (2, 1): 2.0
            ├── 5: (2, 2): 3.33
            ├── 1: (2, 3): 0.67
            ├── 2: (2, 4): 1.33
            └── 4: (2, 5): 2.67
        <BLANKLINE>
        >>> ft.merge_children(1, 2, 2)
        >>> print(ft.get_tree_representation(node_info))
        └── None: (1, 1): 10.0
            ├── 3: (2, 1): 2.0
            ├── 5: (2, 2): 4.0
            └── 2: (2, 4): 4.0
        <BLANKLINE>
        """
        children = self.get_children()
        if not children:
            raise Exception('FractalTree.merge_children:There are no children to be merged')
        if sum(lengths) != len(children):
            raise ValueError(
                f'FractalTree.merge_children: Sum of lengths {sum(lengths)} must be the same as length of children {len(children)}')

        def _merge(nodes):
            node_values = [node.get_value() for node in nodes]
            new_value = sum(node_values)
            for node in nodes[1:]:
                self.remove(node)
            nodes[0].change_value(new_value)

        iter_children = iter(children)
        chunks = [list(itertools.islice(iter_children, l)) for l in lengths]

        for chunk in chunks:
            _merge(chunk)

    def reduce_children_by_condition(self, condition: Callable[['FractalTree'], bool]) -> None:
        if not self.get_children():
            raise ValueError(f'{self} has no children to be reduced')
        for child in [child for child in self.get_children() if condition(child)]:
            self.remove(child)
            del child
        reduced_value = sum([child.get_value() for child in self.get_children()])
        factor = self.get_value() / reduced_value
        for child in self.get_children():
            new_value = child.get_value() * factor
            child.change_value(new_value)

        self._children_fractal_values = [child.get_value() for child in self.get_children()]

    def reduce_children_by_size(self, size, mode: FractalTreeReduceChildrenMode = 'backwards', merge_index=None):
        check_type(mode, 'FractalTreeReduceChildrenMode', class_name=self.__class__.__name__,
                   method_name='reduce_children_by_size', argument_name='mode')
        if mode == 'merge':
            if merge_index is None:
                raise TypeError(f'reduce_children.merge_index must be set for mode merge')
            if 0 > merge_index > self.get_size() - 1:
                raise ValueError(
                    f'reduce_children_by_size.merge_index {merge_index} must be a positive int not greater than {self.get_size() - 1}')

        if size > self.get_size() or size < 0:
            raise ValueError(
                f'reduce_children_by_size.size {size} must be a positive int not greater than {self.get_size()}')
        if size == 0:
            pass
        else:
            if mode == 'backwards':
                self.reduce_children_by_condition(
                    lambda child: child.get_fractal_order() < self.get_size() - size + 1)
            elif mode == 'forwards':
                self.reduce_children_by_condition(
                    lambda child: child.get_fractal_order() > size)
            elif mode == 'sieve':
                if size == 1:
                    self.reduce_children_by_condition(condition=lambda child: child.get_fractal_order() not in [1])
                else:
                    ap = ArithmeticProgression(a1=1, an=self.get_size(), n=size)
                    selection = [int(round(x)) for x in ap]
                    self.reduce_children_by_condition(
                        condition=lambda child: child.get_fractal_order() not in selection)
            else:
                merge_lengths = self._get_merge_lengths(size, merge_index)
                self.merge_children(*merge_lengths)

    def set_permutation_index(self, index: Optional[MatrixIndex]) -> None:
        if index is not None:
            check_type(index, 'MatrixIndex', class_name=self.__class__.__name__,
                       method_name='set_permutation_index',
                       argument_name='index')
            size = self.get_permutation_order_matrix().get_size()
            check_matrix_index_values(index, size, size)
        self._permutation_index = index

    def split(self, *proportions):

        if hasattr(proportions[0], '__iter__'):
            proportions = proportions[0]

        proportions = [Fraction(prop) for prop in proportions]

        for prop in proportions:
            value = self.get_value() * prop / sum(proportions)
            new_node = self.__class__(value=value, proportions=self.get_root().proportions, permutation_index=None)
            new_node._fractal_order = self.get_fractal_order()
            self.add_child(new_node)
            new_node.calculate_permutation_index()

        return self.get_children()

    # copy
    def __copy__(self: 'FractalTree') -> 'FractalTree':
        return self.__class__(value=self.get_value(),
                              proportions=self.proportions,
                              main_permutation_order=self.main_permutation_order,
                              permutation_index=self._permutation_index,
                              fertile=self.fertile)