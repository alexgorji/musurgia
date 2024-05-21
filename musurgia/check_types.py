from typing import Any, Optional

NonNegativeInteger = int


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

    def __init__(self, v: Any, t: type, function_name: Optional[str] = None, class_name: Optional[str] = None,
                 method_name: Optional[str] = None, argument_name: Optional[str] = None,
                 property_name: Optional[str] = None, message: Optional[str] = None):
        if not message:
            message = f'Value {v} must be of type {t.__name__} not {v.__class__.__name__}'
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
        self.msg = msg
        super().__init__(msg)


def check_type(v: Any, t: type, function_name: Optional[str] = None, class_name: Optional[str] = None,
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
    if t == NonNegativeInteger:
        try:
            check_non_negative_integer(v)
        except TypeError as err:
            raise MusurgiaTypeError(v, t, function_name, class_name, method_name, argument_name, property_name,
                                    str(err))
    else:
        if not isinstance(v, t):
            raise MusurgiaTypeError(v, t, function_name, class_name, method_name, argument_name, property_name)
    return True


def check_non_negative_integer(value: int) -> bool:
    if not isinstance(value, int) or value < 0:
        raise TypeError(f"NonNegativeInteger value must be a non-negative integer, got {value}")
    return True
