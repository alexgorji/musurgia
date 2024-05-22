from typing import Any, Optional, Union, Literal, Callable, cast

MUSURGIA_TYPES = ['MatrixData', 'MatrixIndex', 'MatrixTransposeMode', 'NonNegativeInteger', 'PermutationOrder',
                  'PositiveInteger']

MusurgiaType = Literal[
    'MatrixData', 'MatrixIndex', 'MatrixTransposeMode', 'NonNegativeInteger', 'PermutationOrder', 'PositiveInteger']


def create_error_message(v: Optional[Any] = None, t: Optional[Union[type, str]] = None,
                         function_name: Optional[str] = None,
                         class_name: Optional[str] = None,
                         method_name: Optional[str] = None, argument_name: Optional[str] = None,
                         property_name: Optional[str] = None, message: Optional[str] = None):
    if not message and not (v or t):
        raise AttributeError('if no message provided v and t must be set')

    if message and (v or t):
        raise AttributeError('if message is provided no v and t can be set')

    if function_name and (property_name or method_name or class_name):
        raise AttributeError('function_name cannot be set with property_name or method_name or class_name')

    if function_name and not argument_name:
        raise AttributeError('After setting function_name argument_name must be set.')

    if class_name and not (property_name or method_name):
        raise AttributeError('After setting class_name property_name or method_name must be set.')

    if method_name and property_name:
        raise AttributeError('method_name and property_name cannot be set together.')

    if method_name and not (argument_name and class_name):
        raise AttributeError('After setting method_name class_name and argument_name must be set.')

    if argument_name and not (function_name or method_name):
        raise AttributeError('After setting argument_name method_name or function_name must be set.')

    if argument_name and property_name:
        raise AttributeError('argument_name and property_name cannot be set together.')

    if property_name and not class_name:
        raise AttributeError('After setting property_name property_name must be set.')

    if not message:
        if isinstance(t, type):
            _type = t.__name__
        else:
            _type = t
        message = f'Value {v} must be of type {_type} not {v.__class__.__name__}'

    if property_name and class_name:
        msg = f'{class_name}.{property_name}: {message}'

    elif function_name and argument_name:
        msg = f'{function_name}:{argument_name}: {message}'

    elif argument_name and method_name and class_name:
        msg = f'{class_name}.{method_name}:{argument_name}: {message}'

    elif argument_name and method_name and not class_name:
        msg = f'{method_name}:{argument_name}: {message}'

    elif argument_name and not method_name and not class_name:
        msg = f'{argument_name}: {message}'
    else:
        msg = f'{message}'
    return msg


def check_musurgia_type_type(value: str) -> bool:
    if value not in MUSURGIA_TYPES:
        raise TypeError(f"MusurgiaType value must be in {MUSURGIA_TYPES}, got {value}")
    return True


class MusurgiaTypeError(TypeError):
    """
    :param t: ``type``
    :param v: ``value``
    :param argument_name: name of the argument which is being checked.
    :param method_name: name of the method which is executing this checking.
    :param obj: ``object`` which the executing method is a part of

    If ``argument_name`` is not set ``method_name`` and ``obj`` have no impact.
    If ``method_name`` is not set ``obj`` has no impact.
    """

    def __init__(self, v: Any, t: Union[type, str], function_name: Optional[str] = None,
                 class_name: Optional[str] = None,
                 method_name: Optional[str] = None, argument_name: Optional[str] = None,
                 property_name: Optional[str] = None, message: Optional[str] = None):
        if message:
            msg = create_error_message(None, None, function_name, class_name, method_name, argument_name, property_name,
                                       message)
        else:
            msg = create_error_message(v, t, function_name, class_name, method_name, argument_name, property_name)

        super().__init__(msg)

    def __setattr__(self, attr: str, value: Any) -> Any:
        raise AttributeError("Trying to set attribute on a frozen instance MusurgiaTypeError")


NonNegativeInteger = int


def check_non_negative_integer_type(value: NonNegativeInteger) -> bool:
    if not isinstance(value, int) or value < 0:
        raise TypeError(f"NonNegativeInteger value must be a non-negative integer, got {value}")
    return True


PositiveInteger = int


def check_positive_integer_type(value: PositiveInteger) -> bool:
    if not isinstance(value, int) or value <= 0:
        raise TypeError(f"PositiveInteger value must be a positive integer, got {value}")
    return True


PermutationOrder = tuple[int, ...]


def check_permutation_order_type(value: PermutationOrder) -> bool:
    if not isinstance(value, tuple) or len(value) != len(set(value)) or set(value) != set(range(1, len(value) + 1)):
        raise TypeError(
            f"PermutationOrder value must be a tuple with all integers from 1 to an upper limit corresponding the size of input_list, got {value}")
    return True


def check_permutation_order_values(permutation_order: PermutationOrder, size: NonNegativeInteger) -> bool:
    check_type(v=size, t='NonNegativeInteger', function_name='check_permutation_order_values', argument_name='size')
    if len(permutation_order) != size:
        raise ValueError(f"PermutationOrder {permutation_order} must be of size {size}")
    return True


MatrixData = list[list[Any]]


def check_matrix_data_type(matrix_data: MatrixData) -> bool:
    row_size = None
    for i, row in enumerate(matrix_data):
        if not isinstance(row, list):
            raise TypeError(f"TypeMatrix: row {row} is not a list")
        if i == 0:
            row_size = len(row)
        else:
            if len(row) != row_size:
                raise TypeError(f"TypeMatrix: row {row} must be of length {row_size}")
    return True


MatrixIndex = tuple[PositiveInteger, PositiveInteger]


def check_matrix_index_type(index: MatrixIndex) -> bool:
    if not isinstance(index, tuple) or len(index) != 2 or not check_positive_integer_type(
            index[0] or not check_positive_integer_type(index[1])):
        raise TypeError(f"MatrixIndex: index {index} must be a tuple with two positive integers")
    return True


def check_matrix_index_values(index: MatrixIndex, number_of_rows: PositiveInteger,
                              number_of_columns: PositiveInteger) -> bool:
    check_positive_integer_type(number_of_rows)
    check_positive_integer_type(number_of_columns)
    if index[0] > number_of_rows or index[1] > number_of_columns:
        raise ValueError(
            f"MatrixIndex: index {index} must be in ranges (1..{number_of_rows}, 1..{number_of_columns}) ")

    return True


MatrixTransposeMode = Literal['regular', 'diagonal']


def check_matrix_transpose_mode_type(value: MatrixTransposeMode) -> bool:
    permitted = ['regular', 'diagonal']
    if value not in permitted:
        raise TypeError(f"MatrixTransposeMode value must be in {permitted}, got {value}")
    return True


def _get_name_of_check_type_function(musurgia_type: MusurgiaType) -> str:
    """
    >>> _get_name_of_check_type_function("MatrixIndex")
    'check_matrix_index_type'
    """
    return 'check' + ''.join([f'_{x.lower()}' if x.isupper() else x for x in musurgia_type]) + '_type'


def get_check_musurgia_type(musurgia_type: MusurgiaType) -> Callable[[Any], bool]:
    if musurgia_type not in MUSURGIA_TYPES:
        raise TypeError(f'check_musurgia_type: invalid musurgia_type {musurgia_type}')
    check_function_name = _get_name_of_check_type_function(musurgia_type)
    try:
        func: Callable[[Any], bool] = globals()[check_function_name]
    except KeyError:
        raise AttributeError(f'get_check_musurgia_type: {check_function_name} does not exist')
    return func


def check_type(v: Any, t: Union[type, str], function_name: Optional[str] = None, class_name: Optional[str] = None,
               method_name: Optional[str] = None, argument_name: Optional[str] = None,
               property_name: Optional[str] = None) -> bool:
    """
    :param v: ``value`` to be checked.
    :param t: ``type``.
    :param function_name: see :obj:`MusurgiaTypeError`
    :param class_name: see :obj:`MusurgiaTypeError`
    :param method_name: see :obj:`MusurgiaTypeError`
    :param argument_name: see :obj:`MusurgiaTypeError`
    :param property_name: see :obj:`MusurgiaTypeError`

    :raise: :obj:`MusurgiaTypeError`
    """

    def _create_error(message: Optional[str] = None) -> MusurgiaTypeError:
        return MusurgiaTypeError(v, t, function_name, class_name, method_name, argument_name, property_name, message)

    if isinstance(t, type):
        if not isinstance(v, t):
            raise _create_error()
    else:
        check_musurgia_type_type(t)
        try:
            get_check_musurgia_type(cast(MusurgiaType, t))(v)
        except TypeError as err:
            raise _create_error(message=str(err))
    return True
