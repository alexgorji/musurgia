from math import floor, ceil

from fractions import Fraction
from typing import Literal

from musurgia.musurgia_types import ConvertibleToFraction, convert_to_fraction


def _find_nearest_quantized_value(
    quantized_values: list[Fraction], values: list[Fraction]
) -> list[tuple[Fraction, Fraction]]:
    output = []
    for value in values:
        nearest_quantized = min(
            enumerate(quantized_values), key=lambda x: abs(x[1] - value)
        )[1]
        delta = nearest_quantized - value
        output.append((nearest_quantized, delta))
    return output


def _find_quantized_locations(
    positions: list[Fraction], grid_size: ConvertibleToFraction
) -> list[Fraction]:
    grid_size = convert_to_fraction(grid_size)

    def get_quantized(val: Fraction, key: Literal["min", "max"]) -> Fraction:
        factor = Fraction(1, grid_size)
        if key == "min":
            output = Fraction(ceil(val * factor), factor)
        elif key == "max":
            output = Fraction(floor(val * factor), factor)
        else:
            raise ValueError()
        return output

    min_location = Fraction(get_quantized(min(positions), "min"))
    output = [min_location]
    max_location = Fraction(get_quantized(max(positions), "max"))

    while output[-1] < max_location:
        output.append(output[-1] + Fraction(grid_size))

    return output


def get_quantized_positions(
    positions: list[Fraction], grid_size: ConvertibleToFraction
) -> list[Fraction]:
    def _get_quantized_locations() -> list[Fraction]:
        return _find_quantized_locations(positions, grid_size)

    quantized_positions = [
        f[0]
        for f in _find_nearest_quantized_value(_get_quantized_locations(), positions)
    ]

    return quantized_positions


def get_quantized_values(
    values: list[Fraction], grid_size: ConvertibleToFraction
) -> list[Fraction]:
    # print("vals", vals)
    def _get_positions() -> list[Fraction]:
        positions = [Fraction(0)]
        for val in values:
            positions.append(positions[-1] + val)
        return positions

    positions = _get_positions()
    quantized_positions = get_quantized_positions(positions, grid_size)
    quantized_vals = []
    for index in range(len(values)):
        quantized_val = Fraction(
            quantized_positions[index + 1] - quantized_positions[index]
        ).limit_denominator(1000)
        quantized_vals.append(quantized_val)

    return quantized_vals


def find_best_quantized_values(
    values: list[Fraction],
    list_of_grids: list[ConvertibleToFraction],
    check_sum: bool = True,
) -> list[Fraction]:
    if check_sum:
        new_value_grids = []
        for grid in list_of_grids:
            if sum(values) % grid == 0:
                new_value_grids.append(grid)
        if not new_value_grids:
            raise AttributeError("all duration_units failed check_sum")
    else:
        new_value_grids = list_of_grids
    output = values
    old_delta = None
    for grid in new_value_grids:
        quantized_values = get_quantized_values(values, grid)
        new_delta = sum(
            [
                abs(quantized - original)
                for quantized, original in zip(quantized_values, values)
            ]
        )
        if old_delta is None or new_delta < old_delta:
            old_delta = new_delta
            output = quantized_values
    return output
