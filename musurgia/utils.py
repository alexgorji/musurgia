from fractions import Fraction
from typing import Any, Iterator, Literal, Optional, Sequence

from musurgia.musurgia_types import ConvertibleToFraction, convert_to_fraction
from musurgia.quantize import get_quantized_positions


def dToX(
    input_list: Sequence[ConvertibleToFraction],
    first_element: ConvertibleToFraction = 0,
) -> list[Fraction]:
    input = convert_to_fraction_list(input_list)
    output = [convert_to_fraction(first_element)]
    for i in range(len(input)):
        output.append(input[i] + output[i])
    return output


def xToD(input_list: Sequence[ConvertibleToFraction]) -> list[Fraction]:
    input = convert_to_fraction_list(input_list)
    result = []
    for i in range(1, len(input)):
        result.append(input[i] - input[i - 1])
    return result


def flatten(input: list[Any]) -> list[Any]:
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
