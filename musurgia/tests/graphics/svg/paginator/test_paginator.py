from decimal import Decimal
from pathlib import Path
from unittest import TestCase
import pytest
import svg

from musurgia.graphics.geometry import (
    LineOrientation,
    Paddings,
    Margins,
    Position,
    Size,
)
from musurgia.graphics.page_layout import PageLayout
from musurgia.graphics.ruler import Ruler
from musurgia.graphics.svg.paginator import (
    SVGPage,
    SVGPageRow,
    SVGPaginator,
    convert_drawobjects_to_svg_group,
    create_page_rows,
    get_row_content_positions,
)
from musurgia.tests.helpers.svg import SVGTestCase

this_path = Path(__file__)


class SVGPaginatorTestCase(TestCase):
    def test_svg_page_with_one_row(self):
        page = SVGPage()
        page_size = page.get_layout().get_size()
        row = SVGPageRow(
            height=page_size.height,
            paddings=Paddings(10, 20, 30, 40),
        )
        page.add_row(row)
        assert page.get_rows() == [row]
        t, r, b, l = row.get_paddings().to_values()
        assert page.get_row_effective_size(1) == Size(
            page_size.width - r - l, row.get_height() - t - b
        )

    def test_svg_page_create_rows(self):
        page = SVGPage()
        rows = create_page_rows(
            page,
            number_of_rows=3,
            options={
                1: {"paddings": Paddings(10, 20, 30, 40)},
                2: {"paddings": Paddings(10, 20, 30, 40)},
                3: {"paddings": Paddings(10, 20, 30, 40)},
            },
        )
        assert page.get_rows() == rows
        assert len(page.get_rows()) == 3

    def test_svg_page_multiple_rows(self):
        page = SVGPage(layout=PageLayout(margins=Margins(20, 10, 10, 10)))
        create_page_rows(
            page,
            number_of_rows=3,
            options={
                1: {"paddings": Paddings(10, 20, 30, 40)},
                2: {"paddings": Paddings(10, 20, 30, 40)},
                3: {"paddings": Paddings(10, 20, 30, 40)},
            },
        )
        row_height = Decimal(page.get_layout().get_effective_size().height / 3)

        for i, row in enumerate(page.get_rows()):
            assert row.get_height() == row_height
            t, r, b, l = row.get_paddings().to_values()
            assert page.get_row_effective_size(i + 1) == Size(
                page.get_layout().get_effective_size().width - r - l,
                row.get_height() - t - b,
            )
        assert (
            sum([r.get_height() for r in page.get_rows()])
            == page.get_layout().get_effective_size().height
        )

    def test_get_row_content_positions(self):
        page = SVGPage(layout=PageLayout(margins=Margins(20, 10, 10, 10)))
        row_height = Decimal(page.get_layout().get_effective_size().height / 3)

        rows = [
            SVGPageRow(height=row_height, paddings=Paddings(0, 10, 10, 10))
            for _ in range(3)
        ]
        for row in rows:
            page.add_row(row)

        assert get_row_content_positions(page) == [
            Position(20, 20),
            Position(20, 20 + row_height),
            Position(20, 20 + row_height * 2),
        ]

    def test_make_clip_path(self):
        clip_path = SVGPaginator.make_clip_path(Size(100, 200), "clip_path")
        assert (
            clip_path.as_str()
            == '<clipPath id="clip_path"><rect x="0" y="0" width="100" height="200"/></clipPath>'
        )

    def test_get_clipped_svg_group(self):
        ruler = Ruler(type=LineOrientation.HORIZONTAL, length=1000)

        clipped_ruler_svg_group = SVGPaginator.get_clipped_svg_group(
            svg_group=convert_drawobjects_to_svg_group([(Position(0, 0), ruler)]),
            offset=100,
            size=Size(200, ruler.size.height),
        )
        assert isinstance(clipped_ruler_svg_group, svg.G)

    def test_paginate(self):
        ruler = Ruler(type=LineOrientation.HORIZONTAL, length=4 * 205)
        ruler.build()
        paginator = SVGPaginator()
        pages = paginator.paginate(ruler)
        assert len(pages) == 4
        for p in pages:
            assert isinstance(p, SVGPage)
            assert len(p.get_rows()) == 1
            assert isinstance(p.get_rows()[0].get_svg_group(), svg.G)

    def test_paginate_multiple_rows(self):
        ruler = Ruler(type=LineOrientation.HORIZONTAL, length=1000)
        ruler.build()
        page = SVGPage(layout=PageLayout(margins=Margins(20, 10, 10, 10)))
        create_page_rows(
            page,
            number_of_rows=3,
            options={
                1: {"paddings": Paddings(0, 10, 10, 10)},
                2: {"paddings": Paddings(0, 10, 10, 10)},
                3: {"paddings": Paddings(0, 10, 10, 10)},
            },
        )
        paginator = SVGPaginator([page])
        pages = paginator.paginate(ruler)
        assert len(pages) == 2


@pytest.mark.nonci
class SVGPaginatorAsSVG(SVGTestCase):
    def test_page_as_svg_group(self):
        ruler = Ruler(
            type=LineOrientation.HORIZONTAL,
            length=500,
        )
        ruler.options.label.color = "green"
        ruler.build()
        page = SVGPage(layout=PageLayout(margins=Margins(20, 10, 10, 10)))
        page.add_grid()
        page.add_background("white")
        create_page_rows(
            page,
            number_of_rows=4,
            options={
                1: {"paddings": Paddings(0, 10, 10, 10)},
                2: {"paddings": Paddings(0, 10, 10, 10)},
                3: {"paddings": Paddings(0, 10, 10, 10)},
                4: {"paddings": Paddings(0, 10, 10, 10)},
            },
        )
        paginator = SVGPaginator([page])
        page = paginator.paginate(ruler)[0]
        assert isinstance(page.as_svg(), svg.SVG)
        self.compare_page(page, "", this_path, height=210 * 2, width=297 * 2)
