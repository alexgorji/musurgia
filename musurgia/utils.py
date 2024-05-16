from pprint import pprint


class NonNegativeInteger(type):
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

    def __init__(self, v, t, function_name=None, class_name=None, method_name=None, argument_name=None,
                 property_name=None):
        if property_name and class_name:
            msg = f'{class_name}.{property_name}: Value {v} must be of type {t.__name__} not {v.__class__.__name__}.'
        elif function_name and argument_name:
            msg = f'{function_name}.{argument_name}: Value {v} must be of type {t.__name__} not {v.__class__.__name__}.'
        elif argument_name and method_name and class_name:
            msg = f'{class_name}.{method_name}: Value of {argument_name}={v} must be of type {t.__name__} not {v.__class__.__name__}.'

        elif argument_name and method_name and not class_name:
            msg = f'{method_name}: Value of {argument_name}={v} must be of type {t.__name__} not {v.__class__.__name__}.'

        elif argument_name and not method_name and not class_name:
            msg = f'Value of {argument_name}={v} must be of type {t.__name__} not {v.__class__.__name__}.'
        else:
            msg = f'{v} must be of type {t.__name__} not {v.__class__.__name__}.'
        self.msg = msg
        super().__init__(msg)


def check_type(v, t, function_name=None, class_name=None, method_name=None, argument_name=None, property_name=None):
    """
    :param v: ``value`` to be checked.
    :param t: ``type``.
    :param argument_name: see :obj:`MusurgiaTypeError`
    :param method_name: see :obj:`MusurgiaTypeError`
    :param obj: see :obj:`MusurgiaTypeError`

    :raise: :obj:`MusurgiaTypeError`
    """
    if t == NonNegativeInteger:
        if not isinstance(v, int) or v < 0:
            raise MusurgiaTypeError(v, t, function_name, class_name, method_name, argument_name, property_name)
    else:
        if not isinstance(v, t):
            raise MusurgiaTypeError(v, t, function_name, class_name, method_name, argument_name, property_name)


def transpose_3d_vertically(matrix):
    """
    :param matrix:
    :return:

    >>> m = [[('a1', 'b1', 'c1'), ('d1', 'e1', 'f1'), ('g1', 'h1', 'i1')], [('a2', 'b2', 'c2'), ('d2', 'e2', 'f2'), ('g2', 'h2', 'i2')], [('a3', 'b3', 'c3'), ('d3', 'e3', 'f3'), ('g3', 'h3', 'i3')]]
    >>> pprint(m)
    [[('a1', 'b1', 'c1'), ('d1', 'e1', 'f1'), ('g1', 'h1', 'i1')],
     [('a2', 'b2', 'c2'), ('d2', 'e2', 'f2'), ('g2', 'h2', 'i2')],
     [('a3', 'b3', 'c3'), ('d3', 'e3', 'f3'), ('g3', 'h3', 'i3')]]
    >>> pprint(transpose_3d_vertically(m))
    [[('a1', 'a2', 'a3'), ('b1', 'b2', 'b3'), ('c1', 'c2', 'c3')],
     [('d1', 'd2', 'd3'), ('e1', 'e2', 'e3'), ('f1', 'f2', 'f3')],
     [('g1', 'g2', 'g3'), ('h1', 'h2', 'h3'), ('i1', 'i2', 'i3')]]
    """

    output = []
    for column in range(len(matrix)):
        row_list = []
        for element in range(len(matrix)):
            tmp = []
            for row in range(len(matrix)):
                tmp.append(matrix[row][column][element])
            row_list.append(tuple(tmp))
        output.append(row_list)
    return output


def transpose_3d_half_diagonally(matrix):
    """
    :param matrix:
    :return:

    >>> m = [[('a1', 'b1', 'c1'), ('d1', 'e1', 'f1'), ('g1', 'h1', 'i1')], [('a2', 'b2', 'c2'), ('d2', 'e2', 'f2'), ('g2', 'h2', 'i2')], [('a3', 'b3', 'c3'), ('d3', 'e3', 'f3'), ('g3', 'h3', 'i3')]]
    >>> pprint(m)
    [[('a1', 'b1', 'c1'), ('d1', 'e1', 'f1'), ('g1', 'h1', 'i1')],
     [('a2', 'b2', 'c2'), ('d2', 'e2', 'f2'), ('g2', 'h2', 'i2')],
     [('a3', 'b3', 'c3'), ('d3', 'e3', 'f3'), ('g3', 'h3', 'i3')]]
    >>> pprint(transpose_3d_half_diagonally(m))
    [[('a1', 'b2', 'c3'), ('b1', 'c2', 'a3'), ('c1', 'a2', 'b3')],
     [('d1', 'e2', 'f3'), ('e1', 'f2', 'd3'), ('f1', 'd2', 'e3')],
     [('g1', 'h2', 'i3'), ('h1', 'i2', 'g3'), ('i1', 'g2', 'h3')]]
    """

    output = []
    for i in range(len(matrix)):
        row_list = []
        for j in range(len(matrix)):
            tmp = []
            for k in range(len(matrix)):
                row = k
                column = i
                element = (j + k) % len(matrix)
                tmp.append(matrix[row][column][element])
            row_list.append(tuple(tmp))
        output.append(row_list)
    return output


def transpose_3d_diagonally(matrix):
    """
    :param matrix:
    :return:

    >>> m = [[('a1', 'b1', 'c1'), ('d1', 'e1', 'f1'), ('g1', 'h1', 'i1')], [('a2', 'b2', 'c2'), ('d2', 'e2', 'f2'), ('g2', 'h2', 'i2')], [('a3', 'b3', 'c3'), ('d3', 'e3', 'f3'), ('g3', 'h3', 'i3')]]
    >>> pprint(m)
    [[('a1', 'b1', 'c1'), ('d1', 'e1', 'f1'), ('g1', 'h1', 'i1')],
     [('a2', 'b2', 'c2'), ('d2', 'e2', 'f2'), ('g2', 'h2', 'i2')],
     [('a3', 'b3', 'c3'), ('d3', 'e3', 'f3'), ('g3', 'h3', 'i3')]]
    >>> pprint(transpose_3d_diagonally(m))
    [[('a1', 'b2', 'c3'), ('b1', 'c2', 'd3'), ('c1', 'd2', 'e3')],
     [('d1', 'e2', 'f3'), ('e1', 'f2', 'g3'), ('f1', 'g2', 'h3')],
     [('g1', 'h2', 'i3'), ('h1', 'i2', 'a3'), ('i1', 'a2', 'b3')]]
    """

    output = []
    for i in range(len(matrix)):
        row_list = []
        for j in range(len(matrix)):
            tmp = []
            for k in range(len(matrix)):
                row = k
                column = (i + (j + k) // len(matrix)) % len(matrix)
                element = (j + k) % len(matrix)
                tmp.append(matrix[row][column][element])
            row_list.append(tuple(tmp))
        output.append(row_list)
    return output


def flatten(input):
    """
    :param input:
    :return:

    >>> flatten([1, 2])
    [1, 2]
    >>> flatten([1, [2, 3], [4, 5, 6]])
    [1, 2, 3, 4, 5, 6]
    >>> flatten([1, [2, 3], [[4, 5, 6], 7, [8, 9]]])
    [1, 2, 3, 4, 5, 6, 7, 8, 9]

    """
    output = []
    for item in input:
        if isinstance(item, list):
            output.extend(flatten(item))
        else:
            output.append(item)
    return output
