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


def convert_to_fraction_list(input: Sequence[ConvertibleToFraction]) -> list[Fraction]:
    return [convert_to_fraction(x) for x in input]


def convert_to_fraction_tuplet(
    input: Sequence[ConvertibleToFraction],
) -> tuple[Fraction, Fraction]:
    if len(input) != 2:
        raise AttributeError
    return (convert_to_fraction(input[0]), convert_to_fraction(input[1]))


class Normalizer:
    def __init__(
        self,
        input_value_range: tuple[ConvertibleToFraction, ConvertibleToFraction],
        normalization_range: tuple[ConvertibleToFraction, ConvertibleToFraction],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._input_value_range: tuple[ConvertibleToFraction, ConvertibleToFraction] = (
            convert_to_fraction_tuplet(input_value_range)
        )
        self._normalization_range: tuple[
            ConvertibleToFraction, ConvertibleToFraction
        ] = convert_to_fraction_tuplet(normalization_range)

    @property
    def normalization_range(
        self,
    ) -> tuple[ConvertibleToFraction, ConvertibleToFraction]:
        return self._normalization_range

    @normalization_range.setter
    def normalization_range(
        self, value: tuple[ConvertibleToFraction, ConvertibleToFraction]
    ) -> None:
        self._normalization_range = convert_to_fraction_tuplet(value)
        if not self._normalization_range[0] <= self._normalization_range[1]:
            raise AttributeError

    @property
    def input_value_range(self) -> tuple[ConvertibleToFraction, ConvertibleToFraction]:
        return self._input_value_range

    @input_value_range.setter
    def input_value_range(
        self, value: tuple[ConvertibleToFraction, ConvertibleToFraction]
    ) -> None:
        self._input_value_range = convert_to_fraction_tuplet(value)
        if not self._input_value_range[0] <= self._input_value_range[1]:
            raise AttributeError

    def get_normalized_value(self, value: ConvertibleToFraction) -> Fraction:
        norm_min, norm_max = self.normalization_range
        value_min, value_max = self.input_value_range
        normalized_value = norm_min + (norm_max - norm_min) * (
            (value - value_min) / (value_max - value_min)
        )
        return convert_to_fraction(normalized_value)


DirectionValueType = Literal[1, -1]


class RelativeValueGenerator:
    def __init__(
        self,
        value_range: tuple[ConvertibleToFraction, ConvertibleToFraction],
        directions: list[DirectionValueType],
        proportions: list[ConvertibleToFraction],
        value_grid: Optional[ConvertibleToFraction] = None,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self._calculated_values: list[Fraction]
        self._value_range: tuple[ConvertibleToFraction, ConvertibleToFraction] = (
            convert_to_fraction_tuplet(value_range)
        )
        self._directions: list[DirectionValueType] = directions
        self._proportions: list[Fraction] = convert_to_fraction_list(proportions)
        self._value_grid: Optional[ConvertibleToFraction] = (
            None if not value_grid else convert_to_fraction(value_grid)
        )

        self._calculate_intervals()
        self._normalizer: Normalizer
        self._set_normalizer()
        self._calculate_result_values()

    def _calculate_intervals(self) -> None:
        self._intervals = [
            proportion * direction
            for proportion, direction in zip(self.proportions, self.directions)
        ]

    def _get_input_values(self) -> list[Fraction]:
        return dToX(self._intervals)

    def _set_normalizer(self) -> None:
        input_values = self._get_input_values()
        self._normalizer = Normalizer(
            input_value_range=(min(input_values), max(input_values)),
            normalization_range=self.value_range,
        )

    def _calculate_result_values(self) -> None:
        normalized_values = [
            self._normalizer.get_normalized_value(value)
            for value in self._get_input_values()
        ]
        if self.value_grid:
            self._calculated_values = get_quantized_positions(
                normalized_values, grid_size=self.value_grid
            )
        else:
            self._calculated_values = normalized_values

    @property
    def value_range(self) -> tuple[ConvertibleToFraction, ConvertibleToFraction]:
        return self._value_range

    @value_range.setter
    def value_range(
        self, value: tuple[ConvertibleToFraction, ConvertibleToFraction]
    ) -> None:
        self._value_range = convert_to_fraction_tuplet(value)
        self._set_normalizer()
        self._calculate_result_values()

    @property
    def directions(self) -> list[DirectionValueType]:
        return self._directions

    @directions.setter
    def directions(self, value: list[DirectionValueType]) -> None:
        self._directions = value
        self._calculate_intervals()
        self._calculate_result_values()

    @property
    def proportions(self) -> list[Fraction]:
        return self._proportions

    @proportions.setter
    def proportions(self, value: Sequence[ConvertibleToFraction]) -> None:
        self._proportions = convert_to_fraction_list(value)
        self._calculate_intervals()
        self._set_normalizer()
        self._calculate_result_values()

    @property
    def value_grid(self) -> Optional[ConvertibleToFraction]:
        return self._value_grid

    @value_grid.setter
    def value_grid(self, value: Optional[ConvertibleToFraction]) -> None:
        self._value_grid = value
        self._calculate_result_values()

    def get_values(self) -> list[Fraction]:
        return self._calculated_values

    def __iter__(self) -> Iterator[Fraction]:
        for val in self.get_values():
            yield val
