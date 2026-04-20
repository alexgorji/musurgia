from pathlib import Path

import pytest

from musurgia.graphics.container import Container
from musurgia.graphics.geometry import Margins
from musurgia.graphics.page_layout import PageLayout
from musurgia.graphics.segmented_line import SegmentedLine
from musurgia.graphics.svg.paginator import SVGPage, SVGPaginator
from musurgia.tests.helpers.utils_for_tests import create_test_valued_tree
from musurgia.trees.treetographic import TreeGraphicFactory
from musurgia.tests.helpers.svg import SVGTestCase


path = Path(__file__)


class TreeGraphicFactoryTest(SVGTestCase):
    def setUp(self):
        self.vt = create_test_valued_tree()
        self.gf = TreeGraphicFactory(self.vt, unit=10, color="blue")

    def test_create_layer_segmented_line(self):
        for i in range(self.vt.get_number_of_layers()):
            sl = self.gf._create_layer_segmented_line(i + 1)
            assert isinstance(sl, SegmentedLine)
            assert sl.get_length() == self.vt.get_value()
            assert len(sl.get_line_segments()) == len(self.vt.get_layer(i + 1))

    def test_create_svg_container(self):
        container = self.gf.create()
        assert isinstance(container, Container)
        page = SVGPage(layout=PageLayout(margins=Margins(20, 10, 10, 10)))
        page.add_grid()
        # create_page_rows(
        #     page,
        #     number_of_rows=4,
        #     options={
        #         1: {"paddings": Paddings(0, 10, 10, 10)},
        #         2: {"paddings": Paddings(0, 10, 10, 10)},
        #         3: {"paddings": Paddings(0, 10, 10, 10)},
        #         4: {"paddings": Paddings(0, 10, 10, 10)},
        #     },
        # )
        paginator = SVGPaginator([page])
        page = paginator.paginate(container)[0]
        self.compare_page(page, "", path, height=210 * 2, width=297 * 2)

    @pytest.mark.wip
    def test_create_svg_container_with_leaves(self):
        self.fail()
