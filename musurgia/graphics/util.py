import copy
from dataclasses import is_dataclass
from decimal import Decimal
from typing import Any
from collections.abc import Mapping

from musurgia.graphics.geometry import Position, Scalar
from musurgia.graphics.geometry import LineOrientation


def overrides_data_class_options(obj: Any, overrides: Mapping[str, Any]) -> None:
    # obj is a dataclass
    # overrides is a dict
    for key, value in overrides.items():
        if not hasattr(obj, key):
            raise ValueError(f"Invalid option: {key}")

        current = getattr(obj, key)

        if isinstance(value, Mapping):
            if not is_dataclass(current):
                raise ValueError(
                    f"Cannot apply nested overrides to non-dataclass field '{key}'"
                )
            overrides_data_class_options(current, value)
        else:
            setattr(obj, key, value)


def override_options_mappings(
    options: Mapping[str, Any], overrides: Mapping[str, Any]
) -> dict[str, Any]:
    overridden = dict(copy.deepcopy(options))

    for key, value in overrides.items():
        if key not in overridden:
            overridden[key] = value
        else:
            current = overridden[key]
            if isinstance(current, Mapping) and isinstance(value, Mapping):
                overridden[key] = override_options_mappings(current, value)
            else:
                overridden[key] = value

    return overridden


def toggle_line_orientation(type: LineOrientation) -> LineOrientation:
    if type.value == "horizontal":
        return LineOrientation.VERTICAL
    return LineOrientation.HORIZONTAL


def toggle_position(position: Position) -> Position:
    return Position(position.y, position.x)


def convert_to_scalar(value: Scalar | float) -> Scalar:
    if isinstance(value, float):
        return Decimal(value)
    return value
