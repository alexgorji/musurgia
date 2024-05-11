from itertools import cycle
from pprint import pprint

from musurgia.utils import transpose_3d_vertically, transpose_3d_half_diagonally, transpose_3d_diagonally, \
    MusurgiaTypeError, check_type


def permute(input_list: list, permutation_order: tuple[int, ...]) -> list:
    """
    Permutes a list of values by reference to another list named permutation_order.
    :param input_list: A list of values to permute
    :param permutation_order: A tuple consisting of all integers between 1 and lenght of input_list - 1 without duplications.
    :return: permuted list of values

    >>> permute([10, 20, 30, 40], [3, 2, 4, 1])
    Traceback (most recent call last):
       ...
    TypeError: permute.permutation_order: Value [3, 2, 4, 1] must be of type tuple not list.

    >>> permute(None, [3, 2, 4, 1])
    Traceback (most recent call last):
       ...
    TypeError: permute.input_list: Value None must be of type list not NoneType.

    >>> permute([10, 20, 30, 40], None)
    Traceback (most recent call last):
       ...
    TypeError: permute.permutation_order: Value None must be of type tuple not NoneType.

    >>> permute([10, 20, 30, 40], (3, 2, 4))
    Traceback (most recent call last):
       ...
    ValueError: Invalid permutation_order (3, 2, 4) for input_list [10, 20, 30, 40]: wrong length

    >>> permute([10, 20, 30, 40], (3, 2, 4, 1, 3))
    Traceback (most recent call last):
       ...
    ValueError: Invalid permutation_order (3, 2, 4, 1, 3) for input_list [10, 20, 30, 40]: wrong length

    >>> permute([10, 20, 30, 40], (3, 2, 4, 5))
    Traceback (most recent call last):
       ...
    ValueError: Invalid permutation_order (3, 2, 4, 5) for input_list [10, 20, 30, 40]: {2, 3, 4, 5} != {1, 2, 3, 4}

    >>> permute([10, 20, 30, 40], (3, 2, 4, 1))
    [30, 20, 40, 10]
    """

    try:
        check_type(input_list, list, function_name='permute', argument_name='input_list')
    except MusurgiaTypeError as err:
        raise TypeError(err)
    try:
        check_type(permutation_order, tuple, function_name='permute', argument_name='permutation_order')
    except MusurgiaTypeError as err:
        raise TypeError(err)

    if len(permutation_order) != len(input_list):
        raise ValueError(f'Invalid permutation_order {permutation_order} for input_list {input_list}: wrong length')

    if set(permutation_order) != set(range(1, len(input_list) + 1)):
        raise ValueError(
            f'Invalid permutation_order {permutation_order} for input_list {input_list}: {set(permutation_order)} != {set(range(1, len(input_list) + 1))}')

    return [input_list[m - 1] for m in permutation_order]


def get_self_permutation_2d(permutation_order: tuple[int, ...]) -> list[tuple[int, ...]]:
    """
    This is a function for applying the `permutation_order` to itself.

    :param permutation_order: A tuple consisting of all integers between 1 and a higher integer

    :return: A list of `permutations_orders`  as a result of applying the `permutation_order` to itself recursively. The
    result has always a length equal to `len(permutation_order)`.
    Each permuted permutation order will be permuted again. If all integers of the original permuation are not in their
    natural order (natural orders=`(1, 2, 3, 4, ...)`) the resulted list will be distinctive. Otherwise there will be duplicates.

    >>> get_self_permutation_2d([4, 2, 3, 1])
    Traceback (most recent call last):
       ...
    TypeError: permute.permutation_order: Value [4, 2, 3, 1] must be of type tuple not list.

    >>> get_self_permutation_2d((3, 1, 2))
    [(3, 1, 2), (2, 3, 1), (1, 2, 3)]

    >>> get_self_permutation_2d((1, 3, 2))
    [(1, 3, 2), (1, 2, 3), (1, 3, 2)]

    >>> get_self_permutation_2d((1, 2, 3))
    [(1, 2, 3), (1, 2, 3), (1, 2, 3)]

    >>> get_self_permutation_2d((3, 1, 4, 2))
    [(3, 1, 4, 2), (4, 3, 2, 1), (2, 4, 1, 3), (1, 2, 3, 4)]

    >>> get_self_permutation_2d((4, 2, 3, 1))
    [(4, 2, 3, 1), (1, 2, 3, 4), (4, 2, 3, 1), (1, 2, 3, 4)]

    """
    output = [permutation_order]

    for i in range(1, len(permutation_order)):
        output.append(tuple(permute(list(output[i - 1]), permutation_order)))

    return output


def get_self_permutation_3d(permutation_order: tuple[int, ...]) -> list[list[tuple[int, ...]]]:
    """
    This is a function for applying the `permutation_order` to itself in a higher order compared to :obj:`get_self_permutation_2d`.
    If :obj:`get_self_permutation_2d` is a two dimensional reflexive operation, :obj:`get_self_permutation_3d` is a three
    dimensional one. 
    
    :param permutation_order: A list consisting of all integers between 1 and a higher integer
    
    :return:

    >>> get_self_permutation_3d([4, 2, 3, 1])
    Traceback (most recent call last):
       ...
    TypeError: permute.permutation_order: Value [4, 2, 3, 1] must be of type tuple not list.

    >>> pprint(get_self_permutation_3d((3, 1, 2)))
    [[(3, 1, 2), (2, 3, 1), (1, 2, 3)],
     [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
     [(2, 3, 1), (1, 2, 3), (3, 1, 2)]]

    >>> pprint(get_self_permutation_3d((1, 3, 2)))
    [[(1, 3, 2), (1, 2, 3), (1, 3, 2)],
     [(1, 3, 2), (1, 3, 2), (1, 2, 3)],
     [(1, 3, 2), (1, 2, 3), (1, 3, 2)]]

    >>> pprint(get_self_permutation_3d((1, 2, 3)))
    [[(1, 2, 3), (1, 2, 3), (1, 2, 3)],
     [(1, 2, 3), (1, 2, 3), (1, 2, 3)],
     [(1, 2, 3), (1, 2, 3), (1, 2, 3)]]

    >>> pprint(get_self_permutation_3d((3, 1, 4, 2)))
    [[(3, 1, 4, 2), (4, 3, 2, 1), (2, 4, 1, 3), (1, 2, 3, 4)],
     [(2, 4, 1, 3), (3, 1, 4, 2), (1, 2, 3, 4), (4, 3, 2, 1)],
     [(1, 2, 3, 4), (2, 4, 1, 3), (4, 3, 2, 1), (3, 1, 4, 2)],
     [(4, 3, 2, 1), (1, 2, 3, 4), (3, 1, 4, 2), (2, 4, 1, 3)]]

    >>> pprint(get_self_permutation_3d((3, 4, 2, 1)))
    [[(3, 4, 2, 1), (2, 1, 4, 3), (4, 3, 1, 2), (1, 2, 3, 4)],
     [(4, 3, 1, 2), (1, 2, 3, 4), (2, 1, 4, 3), (3, 4, 2, 1)],
     [(2, 1, 4, 3), (3, 4, 2, 1), (1, 2, 3, 4), (4, 3, 1, 2)],
     [(1, 2, 3, 4), (4, 3, 1, 2), (3, 4, 2, 1), (2, 1, 4, 3)]]

    >>> pprint(get_self_permutation_3d((4, 2, 3, 1)))
    [[(4, 2, 3, 1), (1, 2, 3, 4), (4, 2, 3, 1), (1, 2, 3, 4)],
     [(1, 2, 3, 4), (1, 2, 3, 4), (4, 2, 3, 1), (4, 2, 3, 1)],
     [(4, 2, 3, 1), (1, 2, 3, 4), (4, 2, 3, 1), (1, 2, 3, 4)],
     [(1, 2, 3, 4), (1, 2, 3, 4), (4, 2, 3, 1), (4, 2, 3, 1)]]
    """

    self_permuted_order = get_self_permutation_2d(permutation_order)
    output = [self_permuted_order]

    for i in range(1, len(self_permuted_order)):
        output.append(permute(list(output[i - 1]), permutation_order))
    return output


# def permute_matrix_rowwise(matrix, main_permutation_order):
#     lp = LimitedPermutation(main_permutation_order=main_permutation_order, input_list=[1, 2, 3, 4, 5, 6, 7])
#     output = []
#     for row in matrix:
#         permutation_order = lp.__next__()
#         output.append(permute(input_list=row, permutation_order=permutation_order))
#     return output
#

#
#
# def invert_matrix(matrix):
#     return [x for x in zip(*matrix)]
#
#
# def permute_matrix_columnwise(matrix, main_permutation_order):
#     inverted_matrix = invert_matrix(matrix)
#     inverted_matrix = permute_matrix_rowwise(inverted_matrix, main_permutation_order)
#     return invert_matrix(inverted_matrix)
#
#
# def permute_matrix(matrix, main_permutation_order):
#     output = permute_matrix_rowwise(matrix, main_permutation_order)
#     return permute_matrix_columnwise(output, main_permutation_order)


class LimitedPermutation:
    """
    LimitedPermutation is inspired from Gérard Grisey's permutation technique.
    >>> lp = LimitedPermutation(('a', 'b', 'c'), (3, 1, 2))
    Traceback (most recent call last):
       ...
    TypeError: LimitedPermutation.input_list: Value ('a', 'b', 'c') must be of type list not tuple.

    >>> lp = LimitedPermutation(['a', 'b', 'c'], [3, 1, 2])
    Traceback (most recent call last):
       ...
    TypeError: permute.permutation_order: Value [3, 1, 2] must be of type tuple not list.

    >>> lp = LimitedPermutation(['a', 'b', 'c'], (3, 1, 2))
    >>> pprint(lp.get_permutation_orders())
    [[(3, 1, 2), (2, 3, 1), (1, 2, 3)],
     [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
     [(2, 3, 1), (1, 2, 3), (3, 1, 2)]]
    >>> elements = [next(lp) for _ in range(6)]
    >>> [(el.value, el.order) for el in elements]
    [('c', 3), ('a', 1), ('b', 2), ('b', 2), ('c', 3), ('a', 1)]

    >>> lp = LimitedPermutation(['a', 'b', 'c'], (3, 1, 2), first_index=(3, 2))
    >>> elements = [next(lp) for _ in range(9)]
    >>> [(el.value, el.order) for el in elements]
    [('a', 1), ('b', 2), ('c', 3), ('c', 3), ('a', 1), ('b', 2), ('c', 3), ('a', 1), ('b', 2)]
    """

    class Element:
        def __init__(self, value, order):
            self.value = value
            '''order of element in the original input_list'''
            self.order = order

    def __init__(self, input_list: list, main_permutation_order: tuple, first_index: tuple = (1, 1),
                 reading_direction: str = 'horizontal'):

        self._input_list = None
        self._main_permutation_order = None
        self._permutation_order_iterator = None
        self._element_generator = None
        self._permutation_orders = None

        self._first_index = None
        self._reading_direction = None

        self.input_list = input_list
        self.main_permutation_order = main_permutation_order
        self.reading_direction = reading_direction

        self.first_index = first_index

    # private methods
    def _get_flatten_permutation_orders(self):
        return [order for orders in self.get_permutation_orders() for order in orders]

    def _populate_permutation_orders(self):
        self._permutation_orders = get_self_permutation_3d(self.main_permutation_order)
        if self.reading_direction == 'vertical':
            self._permutation_orders = transpose_3d_vertically(self._permutation_orders)
        elif self.reading_direction == 'diagonal':
            self._permutation_orders = transpose_3d_diagonally(self._permutation_orders)
        elif self.reading_direction == 'half-diagonal':
            self._permutation_orders = transpose_3d_half_diagonally(self._permutation_orders)
        else:
            pass

    # properties
    @property
    def first_index(self):
        """
        >>> lp = LimitedPermutation(input_list=['a', 'b', 'c'], main_permutation_order=(3, 1, 2), first_index=(6, 5))
        >>> lp.first_index
        (1, 2)

        :return:
        """
        return self._first_index

    @first_index.setter
    def first_index(self, val):
        if not isinstance(val, tuple):
            raise TypeError(f"{val} must be of type tuple")
        m_1 = val[0]
        m_2 = val[1]
        input_length = len(self.input_list)
        m_1, m_2 = (((m_1 - 1) % input_length) + 1 + ((m_2 - 1) // input_length)) % input_length, (
                (m_2 - 1) % input_length) + 1
        if m_1 == 0:
            m_1 = len(self.input_list)
        self._first_index = (m_1, m_2)

    @property
    def input_list(self):
        return self._input_list

    @input_list.setter
    def input_list(self, val):
        try:
            check_type(t=list, v=val, class_name='LimitedPermutation', property_name='input_list')
        except MusurgiaTypeError as err:
            raise TypeError(err)
        self._input_list = val

    @property
    def main_permutation_order(self):
        return self._main_permutation_order

    @main_permutation_order.setter
    def main_permutation_order(self, val):
        self._main_permutation_order = val
        if self.reading_direction:
            self._populate_permutation_orders()

    @property
    def reading_direction(self):
        """
        >>> lp = LimitedPermutation(['a', 'b', 'c'], (3, 1, 2))
        >>> pprint(lp.get_permutation_orders())
        [[(3, 1, 2), (2, 3, 1), (1, 2, 3)],
         [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
         [(2, 3, 1), (1, 2, 3), (3, 1, 2)]]

        >>> lp = LimitedPermutation(['a', 'b', 'c'], (3, 1, 2), reading_direction='vertical')
        >>> pprint(lp.get_permutation_orders())
        [[(3, 1, 2), (1, 2, 3), (2, 3, 1)],
         [(2, 3, 1), (3, 1, 2), (1, 2, 3)],
         [(1, 2, 3), (2, 3, 1), (3, 1, 2)]]

        >>> lp = LimitedPermutation(['a', 'b', 'c'], (3, 1, 2), reading_direction='diagonal')
        >>> pprint(lp.get_permutation_orders())
        [[(3, 2, 1), (1, 3, 1), (2, 3, 2)],
         [(2, 1, 3), (3, 2, 3), (1, 2, 1)],
         [(1, 3, 2), (2, 1, 2), (3, 1, 3)]]

        >>> lp = LimitedPermutation(['a', 'b', 'c'], (3, 1, 2), reading_direction='half-diagonal')
        >>> pprint(lp.get_permutation_orders())
        [[(3, 2, 1), (1, 3, 2), (2, 1, 3)],
         [(2, 1, 3), (3, 2, 1), (1, 3, 2)],
         [(1, 3, 2), (2, 1, 3), (3, 2, 1)]]

        """

        return self._reading_direction

    @reading_direction.setter
    def reading_direction(self, val):
        permitted = ['horizontal', 'vertical', 'diagonal', 'half-diagonal']
        if val not in permitted:
            raise ValueError(f"Invalid reading direction: {val}. Permitted values are: {permitted}")
        self._permutation_orders = None
        self._reading_direction = val
        if self.main_permutation_order:
            self._populate_permutation_orders()

    # methods
    def get_element_generator(self):
        if self._element_generator is None:
            def gen():
                next_permutations = self.get_permutation_order_iterator().__next__()
                while True:
                    for order in next_permutations:
                        yield self.Element(value=self.input_list[order - 1], order=order)

                    next_permutations = self.get_permutation_order_iterator().__next__()

            self._element_generator = gen()

        return self._element_generator

    def get_permutation_order_iterator(self):
        """
        >>> it = LimitedPermutation(input_list=['a', 'b', 'c'], main_permutation_order=(3, 1, 2)).get_permutation_order_iterator()
        >>> next(it)
        (3, 1, 2)
        >>> next(it)
        (2, 3, 1)
        """
        if self._permutation_order_iterator is None:
            self._permutation_order_iterator = cycle(self._get_flatten_permutation_orders())
            if self.first_index is None:
                raise Exception('first_index must be set first')

            first_index = (self.first_index[0] - 1) * len(self.input_list) + (self.first_index[1] - 1)
            for i in range(first_index):
                self._permutation_order_iterator.__next__()

        return self._permutation_order_iterator

    def get_permutation_orders(self):
        """
        >>> pprint(LimitedPermutation(input_list=['a', 'b', 'c'], main_permutation_order=(3, 1, 2)).get_permutation_orders())
        [[(3, 1, 2), (2, 3, 1), (1, 2, 3)],
         [(1, 2, 3), (3, 1, 2), (2, 3, 1)],
         [(2, 3, 1), (1, 2, 3), (3, 1, 2)]]
        """
        return self._permutation_orders

    def __next__(self):
        return self.get_element_generator().__next__()
