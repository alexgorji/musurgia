from pprint import pprint


class NoneNegativeInteger(type):
    pass


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

    def __init__(self, t, v, argument_name=None, method_name=None, obj=None):
        if argument_name and method_name and obj:
            msg = f'{obj}.{method_name}: Value of {argument_name}={v} must be of type {t} not {type(v)}.'

        elif argument_name and method_name and not obj:
            msg = f'{method_name}: Value of {argument_name}={v} must be of type {t} not {type(v)}.'

        elif argument_name and not method_name and not obj:
            msg = f'Value of {argument_name}={v} must be of type {t} not {type(v)}.'
        else:
            msg = f'{v} must be of type {t} not {type(v)}.'
        self.msg = msg
        super().__init__(msg)


def check_type(t, v, argument_name=None, method_name=None, obj=None):
    """
    :param t: ``type``. Possible types are: [``non_negative_int``]
    :param v: ``value`` to be checked.
    :param argument_name: see :obj:`MusurgiaTypeError`
    :param method_name: see :obj:`MusurgiaTypeError`
    :param obj: see :obj:`MusurgiaTypeError`

    :raise: :obj:`MusurgiaTypeError`
    """
    if t == 'non_negative_int':
        if not isinstance(v, int) or v < 0:
            raise MusurgiaTypeError(t, v, argument_name, method_name, obj)
