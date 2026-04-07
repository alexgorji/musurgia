from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Literal


from musurgia.graphics.geometry import Margins, Position, Scalar, Size
from musurgia.graphics.drawobject import (
    DrawObject,
    StraightLineDrawObject,
)

from musurgia.graphics.geometry import LineOrientation
from musurgia.graphics.svg.utils import create_svg_object


type PageSize = Literal["A3", "A4", "A5"]
type PageOrientation = Literal["portrait", "landscape"]


PAGE_SIZES: Dict[PageSize, Size] = {
    "A4": Size(210, 297),
    "A3": Size(297, 420),
}


@dataclass
class PageLayout:
    size: PageSize | Size = "A4"
    orientation: PageOrientation = "portrait"
    margins: Margins = field(default_factory=lambda: Margins(0, 0, 0, 0))

    def get_size(self) -> Size:
        if isinstance(self.size, Size):
            return self.size
        size = PAGE_SIZES[self.size]
        if self.orientation == "landscape":
            return Size(size.height, size.width)
        return size


class Page:
    def __init__(self, layout: PageLayout | None = None):
        self.layout = layout or PageLayout()
        self._positioned_draw_objects: list[tuple[Position, DrawObject]] = []

    def add_draw_object(self, position: Position, draw_object: DrawObject) -> None:
        self._positioned_draw_objects.append((position, draw_object))

    def add_grid(self, thickness: Scalar = Decimal(0.1)) -> None:
        w, h = self.layout.get_size().width, self.layout.get_size().height
        number_of_horizontal_lines = int(h / 10) + 1
        number_of_vertical_lines = int(w / 10) + 1
        for index in range(number_of_horizontal_lines):
            self.add_draw_object(
                Position(0, index * 10),
                StraightLineDrawObject(
                    type=LineOrientation.HORIZONTAL,
                    length=w,
                    thickness=thickness,
                    color="green",
                ),
            )
        for index in range(number_of_vertical_lines):
            self.add_draw_object(
                Position(index * 10, 0),
                StraightLineDrawObject(
                    type=LineOrientation.VERTICAL,
                    length=h,
                    thickness=thickness,
                    color="green",
                ),
            )

    def convert_to_svg_string(self) -> str:
        size = self.layout.get_size()
        height, width = size.height, size.width

        svg_object = create_svg_object(
            width, height, self._positioned_draw_objects, "mm"
        )

        return svg_object.as_str()
