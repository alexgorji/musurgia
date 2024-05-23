from typing import Any


class MatrixIndexException(Exception):
    pass


class MatrixIndexOutOfRangeError(MatrixIndexException):
    pass


class MatrixIndexEndOfRowError(MatrixIndexException, StopIteration):
    pass


class MatrixIndexEndOfMatrixError(MatrixIndexEndOfRowError, StopIteration):
    pass


class MatrixException(Exception):
    pass


class MatrixIsEmptyError(MatrixException):
    def __init__(self) -> None:
        msg = 'Matrix is empty!'
        super().__init__(msg)


class SquareMatrixException(MatrixException):
    pass


class SquareMatrixDataError(SquareMatrixException):
    pass


class PermutationOrderMatrixException(MatrixException):
    pass


class PermutationOrderMatrixDataError(PermutationOrderMatrixException):
    pass


class FractalTreeException(Exception):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)


class PermutationOrderException(Exception):
    pass


class PermutationOrderError(PermutationOrderException):
    pass


class PermutationOrderTypeError(PermutationOrderError, TypeError):
    pass


class PermutationOrderValueError(PermutationOrderError, ValueError):
    pass


class FontException(Exception):
    pass


class MarginedObjectException(Exception):
    pass


class MarginNotSettableError(MarginedObjectException):
    pass


class PositionedObjectException(Exception):
    pass


class RelativePositionNotSettableError(PositionedObjectException):
    pass


class RelativeXNotSettableError(RelativePositionNotSettableError):
    pass


class RelativeYNotSettableError(RelativePositionNotSettableError):
    pass


class ArithmeticProgressionException(Exception):
    pass


class DAndSError(ArithmeticProgressionException):
    def __init__(self, *args):
        msg = 'you cannot set both d an s!'
        super().__init__(msg, *args)
