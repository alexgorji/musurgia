from typing import Optional, Any, TypeVar

from musurgia.musurgia_types import NonNegativeInteger, check_type, PositiveInteger, \
    MatrixData, MatrixIndex, check_matrix_index_values, check_permutation_order_values, \
    create_error_message, PermutationOrder
from musurgia.permutation.limited_permutation import LimitedPermutationOrders


class MatrixException(Exception):
    pass


class MatrixIsEmptyError(MatrixException):
    def __init__(self) -> None:
        msg = 'Matrix is empty!'
        super().__init__(msg)


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
        check_matrix_index_values(element_index, number_of_rows=self.get_row_size(),
                                  number_of_columns=self.get_column_size())
        return self.matrix_data[element_index[0] - 1][element_index[1] - 1]

    def get_transposed_matrix(self: 'T') -> 'T':
        return self.__class__(matrix_data=[list(y) for y in [x for x in zip(*self.matrix_data)]])


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


class SquareMatrixException(MatrixException):
    pass


class SquareMatrixDataError(SquareMatrixException):
    pass


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


class PermutationOrderMatrixException(MatrixException):
    pass


class PermutationOrderMatrixDataError(PermutationOrderMatrixException):
    pass


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
