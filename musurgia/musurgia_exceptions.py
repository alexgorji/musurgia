from typing import Any, Optional


class MatrixIndexException(Exception):
    pass


class MatrixIndexControllerException(Exception):
    pass


class MatrixIndexOutOfRangeError(MatrixIndexException, ValueError):
    pass


class MatrixIndexEndOfRowError(MatrixIndexException, StopIteration):
    pass


class MatrixIndexEndOfMatrixError(MatrixIndexEndOfRowError, StopIteration):
    pass


class MatrixIndexControllerReadingDirectionError(MatrixIndexControllerException):
    def __init__(self, *args: Any):
        super().__init__('MatrixIndexController.get_next_in_row() works only for reading_direction horizontal.', *args)


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


class PermutaionIndexCalculatorException(Exception):
    pass


class PermutationIndexCalculaterNoParentIndexError(PermutaionIndexCalculatorException, ValueError):
    pass


class FractalTreeException(Exception):
    pass


class FractalTreePermutationOrderError(FractalTreeException):
    pass


class FractalTreePermutationIndexError(FractalTreeException, ValueError):
    pass


class FractalTreeSetMainPermutationOrderFirstError(FractalTreeException, ValueError):
    msg = "set root's main_permutation_order first"

    def __init__(self, msg: Optional[str] = None):
        if msg is None:
            msg = self.msg
        super().__init__(msg)


class FractalTreeMergeWrongValuesError(FractalTreeException, ValueError):
    pass


class FractalTreeHasNoChildrenError(FractalTreeException):
    pass


class FractalTreeHasChildrenError(FractalTreeException):
    pass


class FractalTreeNonRootCannotSetMainPermutationOrderError(FractalTreeException):
    pass


class PermutationOrderException(Exception):
    pass


class PermutationOrderError(PermutationOrderException):
    pass


class PermutationOrderTypeError(PermutationOrderError, TypeError):
    pass


class PermutationOrderValueError(PermutationOrderError, ValueError):
    pass


class MarginedObjectException(Exception):
    pass


class MarginNotSettableError(MarginedObjectException):
    pass


class PositionedObjectException(AttributeError):
    pass


class RelativePositionNotSettableError(PositionedObjectException):
    pass


class RelativeXNotSettableError(RelativePositionNotSettableError):
    pass


class RelativeYNotSettableError(RelativePositionNotSettableError):
    pass


class DrawObjectInContainerHasNegativePositionError(PositionedObjectException):
    pass


class SegmentedLineError(Exception):
    pass


class SegmentedLineSegmentHasMarginsError(SegmentedLineError, AttributeError):
    pass


class ArithmeticProgressionException(Exception):
    pass


class DAndSError(ArithmeticProgressionException):
    def __init__(self, *args: Any):
        msg = 'you cannot set both d an s!'
        super().__init__(msg, *args)


class PdfException(Exception):
    pass


class PdfAttributeError(PdfException, AttributeError):
    pass


# clock
class ClockException(Exception):
    pass


class ClockWrongSecondsValueError(ClockException, ValueError):
    pass


class ClockWrongMinutesValueError(ClockException, ValueError):
    pass


class ClockWrongSecondsTypeError(ClockException, TypeError):
    pass


class ClockWrongMinutesTypeError(ClockException, TypeError):
    pass


class ClockWrongHoursTypeError(ClockException, TypeError):
    pass
