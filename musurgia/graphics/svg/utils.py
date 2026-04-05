import copy
import math

from musurgia.graphics.drawobject import DrawObject, Position
from musurgia.graphics.svg.convertors import SVGConverterRegistry


import svg


from typing import Literal, cast

type SVGUnit = Literal["em", "ex", "px", "pt", "pc", "cm", "mm", "in", "%"]


def create_svg_object(
    width: int | float,
    height: int | float,
    positioned_draw_objects: list[tuple[Position, DrawObject]],
    unit: Literal["em", "ex", "px", "pt", "pc", "cm", "mm", "in", "%"] = "mm",
) -> svg.SVG:
    svg_object = svg.SVG(
        width=svg.Length(width, unit),
        height=svg.Length(height, unit),
        viewBox=svg.ViewBoxSpec(0, 0, width, height),
    )

    if positioned_draw_objects:
        if svg_object.elements is None:
            svg_object.elements = []
        for position, draw_object in positioned_draw_objects:
            svg_object.elements.extend(
                SVGConverterRegistry.convert(position, draw_object)
            )
    return svg_object


# SVGPaginator was created by GitHub Copilot.
class SVGPaginator:
    def __init__(
        self,
        element: svg.Element | list[svg.Element],
        element_width: float,
        row_height: float,
        page_width: float,
        page_height: float,
        unit: SVGUnit = "mm",
        clip_id: str = "clip_row",
    ) -> None:
        self.element = svg.G(elements=element) if isinstance(element, list) else element
        self.element_width = element_width
        self.row_height = row_height
        self.page_width = page_width
        self.page_height = page_height
        self.unit: SVGUnit = unit
        self.clip_id = clip_id

        self.num_rows = math.ceil(element_width / page_width)
        self.rows_per_page = max(1, int(page_height / row_height))
        self.num_pages = math.ceil(self.num_rows / self.rows_per_page)

    def _make_clip_path(self) -> svg.ClipPath:
        return svg.ClipPath(
            id=self.clip_id,
            elements=[
                svg.Rect(x=0, y=0, width=self.page_width, height=self.row_height)
            ],
        )

    def _make_row(self, row_index: int, local_index: int) -> svg.G:
        inner = svg.G(
            transform=[svg.Translate(-row_index * self.page_width, 0)],
            clip_path=f"url(#{self.clip_id})",
            elements=[copy.deepcopy(self.element)],
        )
        return svg.G(
            transform=[svg.Translate(0, local_index * self.row_height)],
            elements=cast(list[svg.Element], [inner]),
        )

    def _make_page(self, page_index: int) -> svg.SVG:
        rows_on_page = min(
            self.rows_per_page, self.num_rows - page_index * self.rows_per_page
        )
        page_elements: list[svg.Element] = [self._make_clip_path()]
        for j in range(rows_on_page):
            i = page_index * self.rows_per_page + j
            page_elements.append(self._make_row(i, j))

        actual_height = rows_on_page * self.row_height
        return svg.SVG(
            width=svg.Length(self.page_width, self.unit),
            height=svg.Length(actual_height, self.unit),
            viewBox=svg.ViewBoxSpec(0, 0, self.page_width, actual_height),
            elements=page_elements,
        )

    def paginate(self) -> list[svg.SVG]:
        return [self._make_page(p) for p in range(self.num_pages)]
