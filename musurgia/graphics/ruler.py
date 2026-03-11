from dataclasses import dataclass, field, fields
from typing import Any, Mapping

from musurgia.graphics.drawobject import Container
from musurgia.graphics.util import overrides_data_class_options


@dataclass
class UnitMarkerOptions:
    length: float = 6.0
    thickness: float = 0.2
    color: str = "black"


@dataclass
class UnitDivisionMarkerOptions:
    length: float = 3.0
    thickness: float = 0.1
    color: str = "black"


@dataclass
class UnitStraightLineOptions:
    thickness: float = 0.2
    color: str = "black"


@dataclass
class RulerOptions:
    unit_marker: UnitMarkerOptions = field(default_factory=UnitMarkerOptions)
    unit_division_marker: UnitDivisionMarkerOptions = field(
        default_factory=UnitDivisionMarkerOptions
    )
    straight_line: UnitStraightLineOptions = field(
        default_factory=UnitStraightLineOptions
    )


class RulerUnit(Container):
    def __init__(self, *, length: float, division: int):
        self._length = length
        self._division = division
        self._build()

    def _build(self) -> None:
        pass


class HorizontalRuler(Container):
    def __init__(
        self,
        *,
        length: float,
        unit_length: int | float = 10,
        unit_division: int = 10,
        color: str | None = None,
        thickness: float | None = None,
        options: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__()
        self._length = length
        self._unit_length = unit_length
        self._unit_division = unit_division
        self._options = RulerOptions()
        if color:
            for field in fields(self._options):
                component = getattr(self._options, field.name)
                if hasattr(component, "color"):
                    setattr(component, "color", color)
        if thickness:
            for field in fields(self._options):
                component = getattr(self._options, field.name)
                if hasattr(component, "thickness"):
                    setattr(component, "thickness", thickness)

        if options:
            overrides_data_class_options(self._options, options)

        self._RulerUnits: list[RulerUnit]

        self._build()

    def _build(self) -> None:
        pass
