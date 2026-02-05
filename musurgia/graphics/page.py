from dataclasses import dataclass, field
from turtle import width
from typing import Dict, Literal, TypedDict, cast

import svg

from musurgia.graphics.drawobject import DrawObjectLayout, TextDrawObject


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
        size = cast(Size, dict(PAGE_SIZES[self.size]))
        if self.orientation == "landscape":
            size["height"], size["width"] = size["width"], size["height"]

        return size


class Page:
    def __init__(self, layout: PageLayout | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = layout or PageLayout()
        self._draw_objects = []

    def add_text(self, text: str, relative_x=0, relative_y=0):
        self._draw_objects.append(
            TextDrawObject(
                text=text,
                layout=DrawObjectLayout(relative_x=relative_x, relative_y=relative_y),
            )
        )

    def convert_to_svg_string(self):
        size = self.layout.get_size()
        height, width = size["height"], size["width"]
        svg_object = svg.SVG(
            width=svg.Length(width, "mm"),
            height=svg.Length(height, "mm"),
            viewBox=svg.ViewBoxSpec(0, 0, width, height),
        )

        for draw_object in self._draw_objects:
            if isinstance(draw_object, TextDrawObject):
                text = svg.Text(
                    x=10,
                    y=20,
                    text=draw_object.text,
                    font_size=4.2,  # 12pt * 25.4 / 72 in mm
                    font_family="Helvetica",
                    fill="blue",
                )
                svg_object.elements = [text]
            else:
                raise TypeError
        return svg_object.as_str()
