from pprint import pprint
from typing import Optional, Any, TypeVar

from musurgia.musurgia_exceptions import MatrixIsEmptyError, SquareMatrixDataError, \
    PermutationOrderMatrixDataError, MatrixIndexOutOfRangeError, MatrixIndexEndOfMatrixError, MatrixIndexEndOfRowError, \
    MatrixIndexControllerReadingDirectionError
from musurgia.musurgia_types import NonNegativeInteger, check_type, PositiveInteger, \
    MatrixData, MatrixIndex, check_matrix_index_values, check_permutation_order_values, \
    create_error_message, PermutationOrder, MatrixTransposeMode, MatrixReadingDirection
from musurgia.permutation.limited_permutation import LimitedPermutationOrders


class SimpleMatrix:
    T = TypeVar('T', bound='SimpleMatrix')
    """
    SimpleMatrix is the core class class for representing a list of lists.
    """

    def __init__(self, matrix_data: Optional[MatrixData] = None, *args: Any, **kwargs: Any) -> None:
        self._matrix_data: MatrixData = []
        if matrix_data is None:
            matrix_data = []
        self.matrix_data = matrix_data

    @property
    def is_empty(self) -> bool:
        if not self.matrix_data:
            return True
        return False

    @property
    def matrix_data(self) -> MatrixData:
        return self._matrix_data

    @matrix_data.setter
    def matrix_data(self, val: MatrixData) -> None:
        check_type(val, 'MatrixData', class_name=self.__class__.__name__, property_name='matrix_data')
        self._matrix_data = val

    def get_row_size(self) -> NonNegativeInteger:
        try:
            return len(self.matrix_data[0])
        except IndexError:
            return 0

    def get_column_size(self) -> NonNegativeInteger:
        return len(self.matrix_data)

    def get_row(self, row_number: PositiveInteger) -> list[Any]:
        check_type(v=row_number, t='PositiveInteger', class_name=self.__class__.__name__, method_name="get_column",
                   argument_name='row_number')
        if self.is_empty:
            raise MatrixIsEmptyError()
        if row_number > self.get_column_size():
            raise ValueError(
                f'{self.__class__.__name__}:get_column:column_number must be less than or equal to {self.get_column_size()}')
        return self.matrix_data[row_number - 1]

    def get_column(self, column_number: PositiveInteger) -> list[Any]:
        check_type(v=column_number, t='PositiveInteger', class_name=self.__class__.__name__, method_name="get_column",
                   argument_name='column_number')
        if self.is_empty:
            raise MatrixIsEmptyError()
        if column_number > self.get_row_size():
            raise ValueError(
                f'{self.__class__.__name__}:get_column:column_number must be less than or equal to {self.get_row_size()}')
        return self.get_transposed_matrix().matrix_data[column_number - 1]

    def get_element(self, element_index: MatrixIndex) -> Any:
        if self.is_empty:
            raise MatrixIsEmptyError()
        check_type(v=element_index, t='MatrixIndex', class_name=self.__class__.__name__, method_name="get_element",
                   argument_name='element_index')
        check_matrix_index_values(element_index, number_of_rows=self.get_column_size(),
                                  number_of_columns=self.get_row_size())
        try:
            return self.matrix_data[element_index[0] - 1][element_index[1] - 1]
        except IndexError as err:
            raise IndexError(f'{err}: element_index: {element_index} data: {self.matrix_data}')

    #
    # def get_transposed_matrix(self: 'T', mode: MatrixTransposeMode = 'regular') -> 'T':
    #     return MatrixTransposition.get_transposed_matrix(self, mode=mode)
    #
    def get_transposed_matrix(matrix: 'T', mode: MatrixTransposeMode = 'regular') -> 'T':
        check_type(v=mode, t='MatrixTransposeMode', class_name='MatrixTransposition',
                   method_name='get_transposed_matrix', argument_name='mode')
        controller = MatrixIndexController(number_of_rows=matrix.get_column_size(),
                                           number_of_columns=matrix.get_row_size())
        if mode == 'regular':
            controller.reading_direction = 'vertical'
        elif mode == 'diagonal':
            controller.reading_direction = 'diagonal'
        # indices = list(controller)
        # print(f'matrix: {matrix.matrix_data} indices: {indices}')
        # controller.reset()
        matrix_data = []
        for c in range(controller.number_of_columns):
            matrix_data.append([matrix.get_element(next(controller)) for _ in range(controller.number_of_rows)])
        return matrix.__class__(matrix_data=matrix_data)


#
#
# class MatrixTransposition:
#     T = TypeVar('T', bound='SimpleMatrix')
#
#     @staticmethod
#     def get_transposed_matrix(matrix: 'T', mode: MatrixTransposeMode) -> 'T':
#         check_type(v=mode, t='MatrixTransposeMode', class_name='MatrixTransposition',
#                    method_name='get_transposed_matrix', argument_name='mode')
#         controller = MatrixIndexController(number_of_rows=matrix.get_column_size(),
#                                            number_of_columns=matrix.get_row_size())
#         if mode == 'regular':
#             controller.reading_direction = 'vertical'
#         elif mode == 'diagonal':
#             controller.reading_direction = 'diagonal'
#         # indices = list(controller)
#         # print(f'matrix: {matrix.matrix_data} indices: {indices}')
#         # controller.reset()
#         matrix_data = []
#         for c in range(controller.number_of_columns):
#             matrix_data.append([matrix.get_element(next(controller)) for _ in range(controller.number_of_rows)])
#         return matrix.__class__(matrix_data=matrix_data)


class Matrix(SimpleMatrix):
    T = TypeVar('T', bound='Matrix')

    def add_row(self, row: list[Any]) -> None:
        check_type(v=row, t=list, class_name=self.__class__.__name__, method_name="add_row", argument_name='row')
        if self.get_row_size() and len(row) != self.get_row_size():
            raise ValueError(f"{self.__class__.__name__}:add_row:row must be of size ({self.get_row_size()})")
        self.matrix_data.append(row)

    def remove_row(self, row_number: NonNegativeInteger) -> list[Any]:
        if self.is_empty:
            raise MatrixIsEmptyError()
        check_type(v=row_number, t='PositiveInteger', class_name=self.__class__.__name__, method_name="remove_row",
                   argument_name='row_number')
        if row_number > self.get_column_size():
            raise ValueError(
                f'{self.__class__.__name__}:remove_row:row_number must be less than or equal to {self.get_column_size()}')
        return self.matrix_data.pop(row_number - 1)


class SquareMatrix(SimpleMatrix):
    T = TypeVar('T', bound='SimpleMatrix')

    def __init__(self, matrix_data: MatrixData, *args: Any, **kwargs: Any) -> None:
        if matrix_data is None or matrix_data == []:
            raise SquareMatrixDataError('SquareMatrix.matrix_data cannot be empty or None')
        super().__init__(matrix_data=matrix_data, *args, **kwargs)
        if self.get_row_size() != self.get_column_size():
            raise SquareMatrixDataError(
                f'SquareMatrix.matrix_data: row size {self.get_row_size()} must be equal to column size {self.get_column_size()}')

    def get_size(self) -> NonNegativeInteger:
        return self.get_column_size()


class PermutationOrderMatrixGenerator:
    def __init__(self, main_permutation_order: PermutationOrder):
        self._lp = LimitedPermutationOrders(main_permutation_order)

    @property
    def main_permutation_order(self) -> PermutationOrder:
        return self._lp.main_permutation_order

    @main_permutation_order.setter
    def main_permutation_order(self, value: PermutationOrder) -> None:
        self._lp.main_permutation_order = value

    def generate_permutation_order_matrix(self):
        return PermutationOrderMatrix(matrix_data=self._lp.get_permutation_orders())


class PermutationOrderMatrix(SquareMatrix):
    T = TypeVar('T', bound='SquareMatrix')

    @SquareMatrix.matrix_data.setter
    def matrix_data(self, val):
        check_type(val, 'MatrixData', class_name=self.__class__.__name__, property_name='matrix_data')
        self._check_matrix_data_permutation_orders(val)
        self._matrix_data = val

    def _check_matrix_data_permutation_orders(self, matrix_data: MatrixData) -> bool:
        size = None
        for permutation_order in [_ for row in matrix_data for _ in row]:
            try:
                check_type(v=permutation_order, t='PermutationOrder', class_name=self.__class__.__name__,
                           property_name='matrix_data')
            except TypeError as err:
                raise PermutationOrderMatrixDataError(err)
            if size is None:
                size = len(permutation_order)
            else:
                try:
                    check_permutation_order_values(permutation_order=permutation_order, size=size)
                except ValueError as err:
                    raise PermutationOrderMatrixDataError(
                        create_error_message(class_name=self.__class__.__name__, property_name='matrix_data',
                                             message=str(err)))
        return True


class MatrixIndexController:
    def __init__(self, number_of_rows: NonNegativeInteger, number_of_columns: NonNegativeInteger,
                 first_index: MatrixIndex = (1, 1), reading_direction: MatrixReadingDirection = 'horizontal'):
        self._number_of_rows = None
        self._number_of_columns = None
        self._reading_direction = None
        self._first_index = None
        self._flatten_index = 0

        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.reading_direction = reading_direction

        self.first_index = first_index

    def _convert_flatten_index_to_index_horizontal(self, flatten_index: PositiveInteger) -> MatrixIndex:
        r = flatten_index // self.number_of_columns + 1
        c = flatten_index % self.number_of_columns + 1
        if c == 0:
            c = self.number_of_columns
        return r, c

    def _convert_flatten_index_to_index_diagonal(self, flatten_index: NonNegativeInteger) -> MatrixIndex:
        r = (flatten_index + 1) % self.number_of_rows
        if r == 0:
            r = self.number_of_rows
        c = (r + flatten_index // self.number_of_rows) % self.number_of_columns
        if c == 0:
            c = self.number_of_columns
        return r, c

    def _convert_flatten_index_to_index_vertical(self, flatten_index: NonNegativeInteger) -> MatrixIndex:
        c = flatten_index // self.number_of_rows + 1
        r = flatten_index % self.number_of_rows + 1
        if r == 0:
            r = self.number_of_rows
        return r, c

    def _convert_flatten_index_to_index(self, flatten_index: NonNegativeInteger) -> MatrixIndex:
        check_type(flatten_index, 'NonNegativeInteger', class_name=self.__class__.__name__,
                   method_name='_convert_flatten_index_to_index', argument_name='flatten_index')
        if flatten_index >= self.number_of_rows * self.number_of_columns:
            raise MatrixIndexEndOfMatrixError
        if self.reading_direction == 'horizontal':
            return self._convert_flatten_index_to_index_horizontal(flatten_index)

        elif self.reading_direction == 'diagonal':
            return self._convert_flatten_index_to_index_diagonal(flatten_index)

        elif self.reading_direction == 'vertical':
            return self._convert_flatten_index_to_index_vertical(flatten_index)
        else:
            raise AttributeError(self.reading_direction)

    def _convert_index_to_flatten_index(self, index: MatrixIndex) -> PositiveInteger:
        r = index[0]
        c = index[1]
        if self.reading_direction == 'horizontal':
            flatten_index = c + (r - 1) * self.number_of_columns
            flatten_index -= 1
            return flatten_index
        elif self.reading_direction == 'diagonal':
            flatten_index = (c - 1) * self.number_of_rows + (r - 1) * (
                    (self.number_of_rows * (self.number_of_columns - 1)) + 1)
            flatten_index %= self.number_of_columns * self.number_of_rows
            return flatten_index
        elif self.reading_direction == 'vertical':
            flatten_index = (r - 1) + (c - 1) * self.number_of_rows
            return flatten_index
        else:
            raise AttributeError(self.reading_direction)

    def _get_next_index(self):
        return self._convert_flatten_index_to_index(self._flatten_index)

    @property
    def number_of_rows(self) -> NonNegativeInteger:
        return self._number_of_rows

    @number_of_rows.setter
    def number_of_rows(self, value):
        check_type(value, 'NonNegativeInteger', class_name=self.__class__.__name__, property_name='number_of_rows')
        self._number_of_rows = value
        self.reset()

    @property
    def number_of_columns(self) -> NonNegativeInteger:
        return self._number_of_columns

    @number_of_columns.setter
    def number_of_columns(self, value):
        check_type(value, 'NonNegativeInteger', class_name=self.__class__.__name__, property_name='number_of_columns')
        self._number_of_columns = value
        self.reset()

    @property
    def reading_direction(self) -> MatrixReadingDirection:
        return self._reading_direction

    @reading_direction.setter
    def reading_direction(self, value):
        check_type(value, 'MatrixReadingDirection', class_name=self.__class__.__name__,
                   property_name='reading_direction')
        self._reading_direction = value
        self.reset()

    @property
    def first_index(self) -> Optional[MatrixIndex]:
        return self._first_index

    @first_index.setter
    def first_index(self, value):
        check_type(value, 'MatrixIndex', class_name=self.__class__.__name__, property_name='index')
        check_matrix_index_values(value, self.number_of_rows, self.number_of_columns)
        self._first_index = value
        self._flatten_index = self._convert_index_to_flatten_index(value)

    def get_next_in_row(self):
        if self.reading_direction != 'horizontal':
            raise MatrixIndexControllerReadingDirectionError
        next_index = self._get_next_index()
        if next_index != self.first_index and next_index[1] == 1:
            raise MatrixIndexEndOfRowError
        return self.__next__()

    def get_next_flatten_index(self):
        return self._flatten_index

    def reset(self):
        if self._first_index is not None:
            self.first_index = self._first_index

    def __iter__(self) -> 'MatrixIndexController':
        return self

    def __next__(self) -> MatrixIndex:
        output = self._get_next_index()
        self._flatten_index += 1
        return output
# class PermutationOrderMatrixTransposition:
#     def __init__(self, matrix: PermutationOrderMatrix):
#         self._matrix: Optional[PermutationOrderMatrix] = None
#         self.matrix = matrix
#
#     @property
#     def matrix(self) -> PermutationOrderMatrix:
#         return self._matrix
#
#     @matrix.setter
#     def matrix(self, value: PermutationOrderMatrix) -> None:
#         if not isinstance(value, PermutationOrderMatrix):
#             raise TypeError(create_error_message())
#         if self._matrix is None:
#             self._matrix = value
#         else:
#             raise AttributeError('PermutationOrderMatrixTransposition: matrix cannot be set after initialization')
#
#     @staticmethod
#     def reorder_permutation_order_matrix_data_vertically(matrix_data: MatrixData) -> MatrixData:
#         """
#         No type checking takes place!
#
#         >>> matrix_data = [[('a1', 'b1', 'c1'), ('d1', 'e1', 'f1'), ('g1', 'h1', 'i1')], [('a2', 'b2', 'c2'), ('d2', 'e2', 'f2'), ('g2', 'h2', 'i2')], [('a3', 'b3', 'c3'), ('d3', 'e3', 'f3'), ('g3', 'h3', 'i3')]]
#         >>> pprint(matrix_data)
#         [[('a1', 'b1', 'c1'), ('d1', 'e1', 'f1'), ('g1', 'h1', 'i1')],
#          [('a2', 'b2', 'c2'), ('d2', 'e2', 'f2'), ('g2', 'h2', 'i2')],
#          [('a3', 'b3', 'c3'), ('d3', 'e3', 'f3'), ('g3', 'h3', 'i3')]]
#         >>> pprint(PermutationOrderMatrixTransposition.reorder_permutation_order_matrix_data_vertically(matrix_data))
#         [[('a1', 'a2', 'a3'), ('b1', 'b2', 'b3'), ('c1', 'c2', 'c3')],
#          [('d1', 'd2', 'd3'), ('e1', 'e2', 'e3'), ('f1', 'f2', 'f3')],
#          [('g1', 'g2', 'g3'), ('h1', 'h2', 'h3'), ('i1', 'i2', 'i3')]]
#         """
#         output = []
#         for column in range(len(matrix_data)):
#             row_list = []
#             for element in range(len(matrix_data)):
#                 tmp = []
#                 for row in range(len(matrix_data)):
#                     tmp.append(matrix_data[row][column][element])
#                 row_list.append(tuple(tmp))
#             output.append(row_list)
#         return output
#
#     @staticmethod
#     def reorder_permutation_order_matrix_data_half_diagonally(matrix_data: MatrixData) -> MatrixData:
#         """
#         No type checking takes place!
#
#         >>> matrix_data = [[('a1', 'b1', 'c1'), ('d1', 'e1', 'f1'), ('g1', 'h1', 'i1')], [('a2', 'b2', 'c2'), ('d2', 'e2', 'f2'), ('g2', 'h2', 'i2')], [('a3', 'b3', 'c3'), ('d3', 'e3', 'f3'), ('g3', 'h3', 'i3')]]
#         >>> pprint(matrix_data)
#         [[('a1', 'b1', 'c1'), ('d1', 'e1', 'f1'), ('g1', 'h1', 'i1')],
#          [('a2', 'b2', 'c2'), ('d2', 'e2', 'f2'), ('g2', 'h2', 'i2')],
#          [('a3', 'b3', 'c3'), ('d3', 'e3', 'f3'), ('g3', 'h3', 'i3')]]
#         >>> pprint(PermutationOrderMatrixTransposition.reorder_permutation_order_matrix_data_half_diagonally(matrix_data))
#         [[('a1', 'b2', 'c3'), ('b1', 'c2', 'a3'), ('c1', 'a2', 'b3')],
#          [('d1', 'e2', 'f3'), ('e1', 'f2', 'd3'), ('f1', 'd2', 'e3')],
#          [('g1', 'h2', 'i3'), ('h1', 'i2', 'g3'), ('i1', 'g2', 'h3')]]
#         """
#         output = []
#         for i in range(len(matrix_data)):
#             row_list = []
#             for j in range(len(matrix_data)):
#                 tmp = []
#                 for k in range(len(matrix_data)):
#                     row = k
#                     column = i
#                     element = (j + k) % len(matrix_data)
#                     tmp.append(matrix_data[row][column][element])
#                 row_list.append(tuple(tmp))
#             output.append(row_list)
#         return output
#
#     @staticmethod
#     def reorder_permutation_order_matrix_data_diagonally(matrix_data: MatrixData) -> MatrixData:
#         """
#         No type checking takes place!
#
#         >>> matrix_data = [[('a1', 'b1', 'c1'), ('d1', 'e1', 'f1'), ('g1', 'h1', 'i1')], [('a2', 'b2', 'c2'), ('d2', 'e2', 'f2'), ('g2', 'h2', 'i2')], [('a3', 'b3', 'c3'), ('d3', 'e3', 'f3'), ('g3', 'h3', 'i3')]]
#         >>> pprint(matrix_data)
#         [[('a1', 'b1', 'c1'), ('d1', 'e1', 'f1'), ('g1', 'h1', 'i1')],
#          [('a2', 'b2', 'c2'), ('d2', 'e2', 'f2'), ('g2', 'h2', 'i2')],
#          [('a3', 'b3', 'c3'), ('d3', 'e3', 'f3'), ('g3', 'h3', 'i3')]]
#         >>> pprint(PermutationOrderMatrixTransposition.reorder_permutation_order_matrix_data_diagonally(matrix_data))
#         [[('a1', 'b2', 'c3'), ('b1', 'c2', 'd3'), ('c1', 'd2', 'e3')],
#          [('d1', 'e2', 'f3'), ('e1', 'f2', 'g3'), ('f1', 'g2', 'h3')],
#          [('g1', 'h2', 'i3'), ('h1', 'i2', 'a3'), ('i1', 'a2', 'b3')]]
#         """
#         output = []
#         for i in range(len(matrix_data)):
#             row_list = []
#             for j in range(len(matrix_data)):
#                 tmp = []
#                 for k in range(len(matrix_data)):
#                     row = k
#                     column = (i + (j + k) // len(matrix_data)) % len(matrix_data)
#                     element = (j + k) % len(matrix_data)
#                     tmp.append(matrix_data[row][column][element])
#                 row_list.append(tuple(tmp))
#             output.append(row_list)
#         return output
#
#     def reorder_vertically(self) -> None:
#         self.matrix.matrix_data = self.reorder_permutation_order_matrix_data_vertically(self.matrix.matrix_data)
#
#     def reorder_half_diagonally(self) -> None:
#         self.matrix.matrix_data = self.reorder_permutation_order_matrix_data_half_diagonally(self.matrix.matrix_data)
#
#     def reorder_diagonally(self) -> None:
#         self.matrix.matrix_data = self.reorder_permutation_order_matrix_data_diagonally(self.matrix.matrix_data)
#
#     def reorder(self, mode: PermutationOrderMatrixReorderMode) -> None:
#         if mode == 'diagonally':
#             self.reorder_diagonally()
#         elif mode == 'half_diagonally':
#             self.reorder_half_diagonally()
#         elif mode == 'vertically':
#             self.reorder_vertically()
#         else:
#             raise ValueError()
