from dataclasses import dataclass, field
from typing import Dict, List, Literal, Tuple

import svg

from musurgia.graphics.drawobject import (
    DrawObject,
    Position,
    Size,
)
from musurgia.graphics.svg.convertors import (
    SVGConverterRegistry,
)

type PageSize = Literal["A3", "A4", "A5"]
type PageOrientation = Literal["portrait", "landscape"]


@dataclass
class Margins:
    top: int
    right: int
    bottom: int
    left: int


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
        self._draw_objects: List[Tuple[Position, DrawObject]] = []

    def add_draw_object(self, position: Position, draw_object: DrawObject) -> None:
        self._draw_objects.append((position, draw_object))

    def convert_to_svg_string(self):
        size = self.layout.get_size()
        height, width = size.height, size.width
        svg_object = svg.SVG(
            width=svg.Length(width, "mm"),
            height=svg.Length(height, "mm"),
            viewBox=svg.ViewBoxSpec(0, 0, width, height),
        )

        if self._draw_objects:
            if svg_object.elements is None:
                svg_object.elements = []
            for position, draw_object in self._draw_objects:
                svg_object.elements.extend(
                    SVGConverterRegistry.convert(position, draw_object)
                )

        return svg_object.as_str()
