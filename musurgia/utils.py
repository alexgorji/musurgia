from typing import Type, Any


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


def is_instance_as_string(object_: Any, class_name: str) -> bool:
    if class_name in [str(c.__name__) for c in object_.__class__.__mro__]:
        return True
    else:
        return False
