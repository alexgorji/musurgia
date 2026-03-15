from dataclasses import is_dataclass
from typing import Any, Mapping

from musurgia.graphics.drawobject import Position
from musurgia.graphics.models import LineOrientation


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


def toggle_line_orientation(type: LineOrientation) -> LineOrientation:
    if type.value == "horizontal":
        return LineOrientation.VERTICAL
    return LineOrientation.HORIZONTAL


def toggle_position(position: Position) -> Position:
    return Position(position.y, position.x)
