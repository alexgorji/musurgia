from decimal import Decimal
from pathlib import Path
from typing import Sequence

from musurgia.graphics.drawobject import TextOptions
from musurgia.graphics.page_layout import PageLayout
from verysimpletree import TreeNodeTupleRepresentation


from musurgia.graphics.geometry import Position
from musurgia.graphics.graphicbuilders.valuetree_graphic import (
    ValueTreeGraphic,
)
from musurgia.graphics.segmented_line import Label, LineSegment
from musurgia.graphics.svg.paginator import SVGPage
from musurgia.tests.helpers.svg import SVGTestCase
from musurgia.tests.helpers.utils_for_tests import (
    DemoValueTree,
    test_fractal_structure_list,
)
from musurgia.tests.test_utils import set_ci_tolerance

this_path = Path(__file__)

STRUCTURE: TreeNodeTupleRepresentation[int] = (
    10,
    (4,),
    (
        6,
        (4, (2,), (2,)),
        (2,),
    ),
)


def test_tree_graphic_copies_leaf() -> None:
    vt = DemoValueTree.create_tree_from_tuple(STRUCTURE, ["value"])
    graphic = ValueTreeGraphic(vt)
    assert graphic.get_children()[0] != graphic.get_children()[0].get_children()[0]
    assert (
        graphic.get_children()[0].get_value_tree_node()
        == graphic.get_children()[0].get_children()[0].get_value_tree_node()
    )


def test_tree_graphic_creates_line_segments() -> None:
    vt = DemoValueTree.create_tree_from_tuple(STRUCTURE, ["value"])
    graphic = ValueTreeGraphic(vt)
    for node in graphic.traverse():
        assert isinstance(node.get_line_segment(), LineSegment)


def test_tree_graphic_line_segment_labels() -> None:
    vt = DemoValueTree.create_tree_from_tuple(STRUCTURE, ["value"])
    graphic = ValueTreeGraphic(vt)
    for node in graphic.traverse():
        node.add_label(Label(text=node.get_value_tree_node().get_position_in_tree()))
        assert (
            node.get_line_segment().get_labels()[0].text
            == node.get_value_tree_node().get_position_in_tree()
        )


def test_tree_graphic_line_segment_markers() -> None:
    vt = DemoValueTree.create_tree_from_list(test_fractal_structure_list, ["value"])
    graphic = ValueTreeGraphic(
        vt,
        options={
            "largest_marker_size": 20,
            "marker_length_shrinking_factor": Decimal("0.5"),
        },
    )

    def _get_layer(number: int) -> Sequence[tuple[str, Decimal | int]]:
        return graphic.get_layer(
            number,
            key=lambda n: (
                n.get_value_tree_node().get_position_in_tree(),
                n.get_line_segment().start_marker.length,
            ),
        )

    assert _get_layer(1) == [("1", 20), ("2", 20), ("3", 20), ("4", 20)]
    assert _get_layer(2) == [
        ("1.1", 20),
        ("1.2", 10),
        ("1.3", 10),
        ("1.4", 10),
        ("2", 20),
        ("3.1", 20),
        ("3.2", 10),
        ("3.3", 10),
        ("3.4", 10),
        ("4.1", 20),
        ("4.2", 10),
        ("4.3", 10),
        ("4.4", 10),
    ]
    assert _get_layer(3) == [
        ("1.1", 20),
        ("1.2.1", 10),
        ("1.2.2", 5),
        ("1.2.3", 5),
        ("1.2.4", 5),
        ("1.3", 10),
        ("1.4.1", 10),
        ("1.4.2", 5),
        ("1.4.3", 5),
        ("1.4.4", 5),
        ("2", 20),
        ("3.1", 20),
        ("3.2", 10),
        ("3.3.1", 10),
        ("3.3.2", 5),
        ("3.3.3", 5),
        ("3.3.4", 5),
        ("3.4.1", 10),
        ("3.4.2", 5),
        ("3.4.3", 5),
        ("3.4.4", 5),
        ("4.1.1", 20),
        ("4.1.2", 5),
        ("4.1.3", 5),
        ("4.1.4", 5),
        ("4.2.1", 10),
        ("4.2.2", 5),
        ("4.2.3", 5),
        ("4.2.4", 5),
        ("4.3", 10),
        ("4.4", 10),
    ]


class ValueTreeGraphicBuilderRegressionTestCase(SVGTestCase):
    def test_scaled_one_node_tree(self) -> None:
        tree_structure_tuple: TreeNodeTupleRepresentation[int] = (10, (10,))
        vt = DemoValueTree.create_tree_from_tuple(tree_structure_tuple, ["value"])
        page = SVGPage()
        page.add_grid(thickness=Decimal("0.05"))
        page.add_background("white")
        page.add_grid()
        graphic = ValueTreeGraphic(vt)
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
        tree_structure_list: TreeNodeTupleRepresentation[int] = (
            10,
            (3,),
            (1,),
            (4,),
            (2,),
        )
        vt = DemoValueTree.create_tree_from_tuple(tree_structure_list, ["value"])
        page = SVGPage()
        page.add_grid(thickness=Decimal("0.05"))

        page.add_background("white")
        page.add_grid()
        graphic = ValueTreeGraphic(vt)
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

        page = SVGPage(layout=PageLayout(orientation="landscape"))
        page.add_grid(thickness=Decimal("0.05"))

        page.add_background("white")
        page.add_grid()
        graphic = ValueTreeGraphic(
            vt,
            options={
                "scale": 25,
                "distance_between_layers": 25,
                "largest_marker_size": 10,
            },
        )
        offset = 0
        for node in graphic.traverse():
            level = node.get_value_tree_node().get_level()
            if level == 1:
                y = 3
            elif level == 2:
                y = 5
            else:
                y = 8 + offset
                offset = 2 if offset == 0 else 0

            node.add_label(
                Label(
                    text=node.get_value_tree_node().get_position_in_tree(),
                    offset=Position(0, y),
                    options=TextOptions(font_size=5),
                )
            )
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
