from dataclasses import dataclass, field
from turtle import width
from typing import Dict, Literal, TypedDict, cast

import svg


type PageSize = Literal["A3", "A4", "A5"]
type PageOrientation = Literal["portrait", "landscape"]


class Margins(TypedDict):
    left: int
    right: int
    bottom: int
    top: int


class Size(TypedDict):
    height: int
    width: int


PAGE_SIZES: Dict[PageSize, Size] = {
    "A4": {"height": 297, "width": 210},
    "A3": {"height": 420, "width": 297},
}


@dataclass
class PageLayout:
    size: PageSize | Size = "A4"
    orientation: PageOrientation = "portrait"
    margins: Margins = field(
        default_factory=lambda: cast(
            Margins,
            {
                "left": 0,
                "right": 0,
                "bottom": 0,
                "top": 0,
            },
        )
    )

    def get_size(self) -> Size:
        if isinstance(self.size, dict):
            return self.size
        size = PAGE_SIZES[self.size]
        if self.orientation == "landscape":
            size["height"], size["width"] = size["width"], size["height"]

        return size


class Page:
    def __init__(self, layout: PageLayout | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = layout or PageLayout()

    def convert_to_svg_string(self):
        size = self.layout.get_size()
        height, width = size["height"], size["width"]

        return svg.SVG(
            width=svg.Length(width, "mm"),
            height=svg.Length(height, "mm"),
            viewBox=svg.ViewBoxSpec(0, 0, width, height),
        ).as_str()
