from decimal import Decimal
from pathlib import Path

from verysimpletree.tree import TreeNodeListRepresentation
from musurgia.graphics.geometry import Position

from musurgia.graphics.graphicbuilders.valuetree_graphic import ValueTreeGraphic
from musurgia.graphics.svg.paginator import SVGPage
from musurgia.tests.helpers.svg import SVGTestCase
from musurgia.tests.helpers.utils_for_tests import (
    DemoValueTree,
    test_fractal_structure_list,
)
from musurgia.tests.test_utils import set_ci_tolerance

this_path = Path(__file__)


class ValueTreeGraphicBuilderRegressionTestCase(SVGTestCase):
    def test_scaled_one_node_tree(self) -> None:
        tree_structure_list: TreeNodeListRepresentation[int] = [10, [10]]
        vt = DemoValueTree.create_tree_from_list(tree_structure_list, ["value"])
        page = SVGPage()
        page.add_grid(thickness=Decimal("0.05"))
        page.add_background("white")
        page.add_grid()
        graphic = ValueTreeGraphic(vt, scale=10)
        g_tree = graphic.build()
        page.add_draw_object(Position(10, 10), g_tree)

        self.compare_page(
            page,
            "scaled_one_node",
            this_path,
            height=210 * 2,
            width=297 * 2,
            tolerance=set_ci_tolerance(0.03),
        )

    def test_one_layer_tree(self) -> None:
        tree_structure_list: TreeNodeListRepresentation[int] = [
            10,
            [3],
            [1],
            [4],
            [2],
        ]
        vt = DemoValueTree.create_tree_from_list(tree_structure_list, ["value"])
        page = SVGPage()
        page.add_grid(thickness=Decimal("0.05"))

        page.add_background("white")
        page.add_grid()
        graphic = ValueTreeGraphic(vt, scale=10)
        g_tree = graphic.build()
        page.add_draw_object(Position(10, 10), g_tree)

        self.compare_page(
            page,
            "one_layer",
            this_path,
            height=210 * 2,
            width=297 * 2,
            tolerance=set_ci_tolerance(0.03),
        )

    def test_multiple_layered_tree(self) -> None:
        vt = DemoValueTree.create_tree_from_list(test_fractal_structure_list, ["value"])

        page = SVGPage()
        page.add_grid(thickness=Decimal("0.05"))

        page.add_background("white")
        page.add_grid()
        graphic = ValueTreeGraphic(vt, scale=10)
        g_tree = graphic.build()
        page.add_draw_object(Position(10, 10), g_tree)

        self.compare_page(
            page,
            "multiple_layered",
            this_path,
            height=210 * 2,
            width=297 * 2,
            tolerance=set_ci_tolerance(0.03),
        )
