import copy
from decimal import Decimal
from typing import Any, Mapping

import svg

from musurgia.graphics.container import Container
from musurgia.graphics.drawobject import (
    DrawObject,
    LineOptions,
    Rectangle,
    RectangleOptions,
    StraightLine,
)
from musurgia.graphics.geometry import LineOrientation, Paddings, Position, Scalar, Size
from musurgia.graphics.page_layout import PageLayout
from musurgia.graphics.svg.convertors import SVGConverterRegistry


def convert_drawobjects_to_svg_group(
    positioned_drawobjects: list[tuple[Position, DrawObject]],
) -> svg.G:
    g = svg.G()
    g.elements = []
    for p, d in positioned_drawobjects:
        g.elements.extend(SVGConverterRegistry.convert(p, d))
    return g


def create_page_rows(
    page: "SVGPage",
    number_of_rows: int = 1,
    options: dict[int, Mapping[str, Any]] | None = None,
) -> list["SVGPageRow"]:
    if page.get_rows():
        raise AttributeError("Page has already rows.")
    row_height = Decimal(page.get_layout().get_effective_size().height) / Decimal(
        number_of_rows
    )
    for i in range(number_of_rows):
        row_options = options.get(i + 1) if options else None
        paddings = Paddings()
        if options:
            if row_options := options.get(i + 1):
                _paddings = row_options.get("paddings")
                if isinstance(_paddings, Paddings):
                    paddings = _paddings

        row = SVGPageRow(height=row_height, paddings=paddings)
        page.add_row(row)

    return page.get_rows()


def get_row_content_positions(page: "SVGPage") -> list[Position]:
    positions = []
    t, _, _, l = page.get_layout().margins.to_values()
    y = t
    for row in page.get_rows():
        positions.append(
            Position(l + row.get_paddings().left, y + row.get_paddings().top)
        )
        y += row.get_height()

    return positions


class SVGPageRow:
    def __init__(
        self,
        height: Scalar,
        paddings: Paddings = Paddings(),
    ) -> None:
        self._height = height
        self._paddings = paddings
        self._svg_group: svg.G | None = None
        self._positioned_draw_objects: list[tuple[Position, DrawObject]] = []

    def get_height(self) -> Scalar:
        return self._height

    def get_paddings(self) -> Paddings:
        return self._paddings

    def add_svg_group(self, svg_group: svg.G) -> None:
        self._svg_group = svg_group

    def get_svg_group(self) -> svg.G | None:
        return self._svg_group

    def add_draw_object(self, position: Position, draw_object: DrawObject) -> None:
        self._positioned_draw_objects.append((position, draw_object))


class SVGPage:
    def __init__(self, layout: PageLayout = PageLayout()) -> None:
        self._layout = layout
        self._rows: list[SVGPageRow] = []
        self._grid: list[tuple[Position, DrawObject]] = []
        self._background: Rectangle | None = None

    def get_layout(self) -> PageLayout:
        return self._layout

    def add_draw_object(
        self, position: Position, draw_object: DrawObject, row_number: int = 0
    ) -> None:
        if not self._rows:
            create_page_rows(self, 1)
        try:
            row = self.get_rows()[row_number - 1]
        except IndexError:
            raise AttributeError("Invalid row number")

        row.add_draw_object(position, draw_object)

    def add_row(self, row: SVGPageRow) -> None:
        self._rows.append(row)

    def add_background(self, color: str = "white") -> None:
        self._background = Rectangle(
            size=self.get_layout().get_size(),
            options=RectangleOptions(fillcolor=color, color="white"),
        )

    def add_grid(self, thickness: Scalar = Decimal("0.1")) -> None:
        w, h = self._layout.get_size().width, self._layout.get_size().height
        number_of_horizontal_lines = int(h / 10) + 1
        number_of_vertical_lines = int(w / 10) + 1
        for index in range(number_of_horizontal_lines):
            self._grid.append(
                (
                    Position(0, index * 10),
                    StraightLine(
                        type=LineOrientation.HORIZONTAL,
                        length=w,
                        options=LineOptions(thickness=thickness, color="green"),
                    ),
                ),
            )
        for index in range(number_of_vertical_lines):
            self._grid.append(
                (
                    Position(index * 10, 0),
                    StraightLine(
                        type=LineOrientation.VERTICAL,
                        length=h,
                        options=LineOptions(thickness=thickness, color="green"),
                    ),
                ),
            )

    def get_rows(self) -> list[SVGPageRow]:
        return self._rows

    def get_row_effective_size(self, row_number: int) -> Size:
        row = self.get_rows()[row_number - 1]
        t, r, b, l = row.get_paddings().to_values()
        return Size(
            self._layout.get_effective_size().width - r - l, row.get_height() - t - b
        )

    def copy(self) -> "SVGPage":
        return SVGPage(layout=copy.deepcopy(self.get_layout()))

    def as_svg(self) -> svg.SVG:
        w, h = self.get_layout().get_size().to_values()
        svg_object = svg.SVG(
            width=svg.Length(w, "mm"),
            height=svg.Length(h, "mm"),
            viewBox=svg.ViewBoxSpec(0, 0, w, h),
        )
        row_positions = get_row_content_positions(self)

        svg_object.elements = []

        if self._background:
            background_rectangle_svg_group = convert_drawobjects_to_svg_group(
                [(Position(0, 0), self._background)]
            )
            svg_object.elements.append(background_rectangle_svg_group)

        if self._grid:
            grid_svg_group = convert_drawobjects_to_svg_group(self._grid)
            svg_object.elements.append(grid_svg_group)

        for position, row in zip(row_positions, self.get_rows()):
            if group := row.get_svg_group():
                x, y = position.to_values()
                wrapper = svg.G(
                    transform=[svg.Translate(x=float(x), y=float(y))],
                    elements=[group],
                )
                svg_object.elements.append(wrapper)
            else:
                svg_object.elements.append(
                    convert_drawobjects_to_svg_group(row._positioned_draw_objects)
                )

        return svg_object

    def convert_to_svg_string(self) -> str:
        return self.as_svg().as_str()


class SVGPaginator:
    def __init__(self, pages: list[SVGPage] = [SVGPage()]) -> None:
        self._pages = pages

    @staticmethod
    def make_clip_path(size: Size, clip_id: str) -> svg.ClipPath:
        return svg.ClipPath(
            id=clip_id,
            elements=[svg.Rect(x=0, y=0, width=size.width, height=size.height)],
        )

    @staticmethod
    def get_clipped_svg_group(
        svg_group: svg.G, offset: Scalar, size: Size, clip_id: str = "clip"
    ) -> svg.G:
        clip_path = SVGPaginator.make_clip_path(size=size, clip_id=clip_id)
        return svg.G(
            clip_path=f"url(#{clip_id})",
            elements=[
                svg.Defs(elements=[clip_path]),
                svg.G(
                    transform=[svg.Translate(x=float(-offset), y=0)],
                    elements=[copy.deepcopy(svg_group)],
                ),
            ],
        )

    def paginate(self, container: Container) -> list[SVGPage]:
        page_number = 1
        offset = Decimal(0)
        svg_group = convert_drawobjects_to_svg_group(
            container.get_draw_objects(positioned=True)
        )
        pages = []
        while offset < container.size.width:
            page_index = page_number - 1 if page_number <= len(self._pages) else -1
            try:
                page = self._pages[page_index]
            except IndexError:
                page = self._pages[page_index].copy()
            rows = page.get_rows()
            if not rows:
                rows = create_page_rows(page)
            id = 1
            for i, row in enumerate(rows):
                if offset > container.size.width:
                    break
                row_effective_size = page.get_row_effective_size(i + 1)
                row.add_svg_group(
                    SVGPaginator.get_clipped_svg_group(
                        svg_group, offset, row_effective_size, f"id{id}"
                    )
                )
                id += 1
                offset += row_effective_size.width
            pages.append(page)
            page_number += 1
        return pages
