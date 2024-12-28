from fractions import Fraction
import os
import unittest
from pathlib import Path

from diff_pdf_visually import pdf_similar  # type: ignore

from musurgia.trees.fractaltimelinetree import FractalTimelineTree
from musurgia.pdf import TextLabel, DrawObjectColumn, StraightLine
from musurgia.pdf.drawobject import MasterDrawObject
from musurgia.trees.musicaltree import FractalMusicalTree, FractalRelativeMusicTree, TreeChordFactory
from musurgia.trees.timelinetree import TimelineDuration, TimelineTree
from musurgia.trees.valuedtree import ValuedTree

test_fractal_structur_list = [
    Fraction(10, 1),
    [
        Fraction(3, 1),
        [Fraction(3, 5)],
        [
            Fraction(6, 5),
            [Fraction(6, 25)],
            [Fraction(12, 25)],
            [Fraction(3, 25)],
            [Fraction(9, 25)],
        ],
        [Fraction(3, 10)],
        [
            Fraction(9, 10),
            [Fraction(27, 100)],
            [Fraction(9, 100)],
            [Fraction(9, 25)],
            [Fraction(9, 50)],
        ],
    ],
    [Fraction(1, 1)],
    [
        Fraction(4, 1),
        [Fraction(2, 5)],
        [Fraction(4, 5)],
        [
            Fraction(6, 5),
            [Fraction(6, 25)],
            [Fraction(12, 25)],
            [Fraction(3, 25)],
            [Fraction(9, 25)],
        ],
        [
            Fraction(8, 5),
            [Fraction(4, 25)],
            [Fraction(8, 25)],
            [Fraction(12, 25)],
            [Fraction(16, 25)],
        ],
    ],
    [
        Fraction(2, 1),
        [
            Fraction(4, 5),
            [Fraction(4, 25)],
            [Fraction(8, 25)],
            [Fraction(2, 25)],
            [Fraction(6, 25)],
        ],
        [
            Fraction(3, 5),
            [Fraction(9, 50)],
            [Fraction(3, 50)],
            [Fraction(6, 25)],
            [Fraction(3, 25)],
        ],
        [Fraction(2, 5)],
        [Fraction(1, 5)],
    ],
]


def create_test_path(path, test_name):
    return path.parent.joinpath(f"{path.stem}_{test_name}")


class FilePath:
    def __init__(self, unittest, parent_path, name, extension):
        self._unittest = None
        self._parent_path = None
        # self._name = None
        # self._extension = None

        self.unittest = unittest
        self.parent_path = parent_path
        self.name = name
        self.extension = extension
        self.out_path = None

    @property
    def unittest(self):
        return self._unittest

    @unittest.setter
    def unittest(self, val):
        # if not isinstance(val, PdfTestCase):
        #     raise TypeError(f"unittest.value must be of type {type(PdfTestCase)} not{type(val)}")
        self._unittest = val

    @property
    def parent_path(self):
        return self._parent_path

    @parent_path.setter
    def parent_path(self, val):
        if not isinstance(val, Path):
            raise TypeError(
                f"parent_path.value must be of type {type(Path)} not{type(val)}"
            )
        self._parent_path = val

    def __enter__(self):
        self.out_path = create_test_path(
            self.parent_path, self.name + "." + self.extension
        )
        return self.out_path

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unittest.assertCompareFiles(self.out_path)


class PdfTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _compare_pdfs(self, actual_file_path, expected_file_path, verbosity):
        self.assertTrue(
            pdf_similar(actual_file_path, expected_file_path, verbosity=verbosity)
        )

    def _compare_contents(self, actual_file_path, expected_file_path):
        with open(actual_file_path, "r") as myfile:
            result = myfile.read()

        with open(expected_file_path, "r") as myfile:
            expected = myfile.read()

        self.assertEqual(expected, result)

    def assertCompareFiles(
        self, actual_file_path, expected_file_path=None, verbosity=0
    ):
        file_name, extension = os.path.splitext(actual_file_path)
        if not expected_file_path:
            if not extension:
                raise ValueError("actual_file_path has no file extension")
            expected_file_path = file_name + "_expected" + extension

        if extension == ".pdf":
            self._compare_pdfs(
                actual_file_path, expected_file_path, verbosity=verbosity
            )
        else:
            self._compare_contents(actual_file_path, expected_file_path)

    def file_path(self, parent_path, name, extension):
        tfp = FilePath(self, parent_path, name, extension)
        return tfp


class XMLTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _compare_contents(self, actual_file_path, expected_file_path):
        with open(actual_file_path, "r") as myfile:
            result = myfile.read()

        with open(expected_file_path, "r") as myfile:
            expected = myfile.read()

        self.assertEqual(expected, result)

    def assertCompareFiles(self, actual_file_path, expected_file_path=None):
        file_name, extension = os.path.splitext(actual_file_path)
        if not expected_file_path:
            if not extension:
                expected_file_path += ".xml"
            expected_file_path = file_name + "_expected" + ".xml"

        self._compare_contents(actual_file_path, expected_file_path)

    def file_path(self, parent_path, name):
        tfp = FilePath(self, parent_path, name, "xml")
        return tfp


def fractal_node_info(node):
    return f"{node.get_fractal_order()}: {node.get_permutation_index()}: {round(float(node.get_value()), 2)}"


def fractal_node_info_with_permutation_order(node):
    return f"{node.get_fractal_order()}: {node.get_permutation_index()}: {node.get_permutation_order()}: {round(float(node.get_value()), 2)}"


class DummyMaster(MasterDrawObject):
    def get_slave_margin(self, slave, margin):
        return 10

    def get_slave_position(self, slave, position):
        return 20

    def draw(self, pdf):
        pass

    def get_relative_x2(self):
        pass

    def get_relative_y2(self):
        pass


def add_control_positions_to_draw_object(draw_object):
    text_1 = TextLabel(draw_object.positions, font_size=8)
    text_2 = TextLabel(
        draw_object.get_end_positions(),
        placement="below",
        font_size=8,
        left_margin=(draw_object.get_relative_x2() - draw_object.relative_x),
    )

    draw_object.add_text_label(text_1)
    draw_object.add_text_label(text_2)


numbers = ["one", "two", "three"]


def add_test_left_labels(drawobject):
    for t in numbers:
        drawobject.add_text_label(f"left label {t}", placement="left", font_size=8)


def add_test_below_labels(drawobject):
    for t in numbers:
        drawobject.add_text_label(f"below label {t}", placement="below", font_size=8)


# def add_test_right_labels(drawobject):
#     for t in numbers:
#         drawobject.add_text_label(f'right label {t}', placement='right', font_size=8)


def add_test_above_labels(drawobject):
    for t in numbers:
        drawobject.add_text_label(f"above label {t}", placement="above", font_size=8)


def add_test_right_above_labels(drawobject):
    for t in numbers:
        drawobject.add_text_label(
            f"right above label {t}", placement="right_above", font_size=8
        )


def add_test_right_below_labels(drawobject):
    for t in numbers:
        drawobject.add_text_label(
            f"right below label {t}", placement="right_below", font_size=8
        )


def add_test_labels(drawobject):
    add_test_above_labels(drawobject)
    add_test_below_labels(drawobject)
    add_test_left_labels(drawobject)
    # add_test_right_labels(drawobject)
    # add_test_right_above_labels(drawobject)
    # add_test_right_below_labels(drawobject)


def create_simple_column(list_of_draw_objects):
    c = DrawObjectColumn(show_borders=True, show_margins=True)
    for do in list_of_draw_objects:
        do.relative_y = 5
        do.margins = (10, 10, 10, 10)
    divider = StraightLine("h", max([do.get_width() for do in list_of_draw_objects]))
    for do in list_of_draw_objects:
        c.add_draw_object(do)
        if do != list_of_draw_objects[-1]:
            c.add_draw_object(divider)

    return c


def create_test_fractal_timline_tree():
    ft = FractalTimelineTree(
        duration=TimelineDuration(10),
        proportions=(1, 2, 3, 4),
        main_permutation_order=(3, 1, 4, 2),
        permutation_index=(1, 1),
    )
    ft.add_layer()

    ft.add_layer(lambda node: node.get_fractal_order() > 1)
    ft.add_layer(lambda node: node.get_fractal_order() > 2)
    return ft


def create_test_fractal_musical_tree():
    ft = FractalMusicalTree(
        duration=TimelineDuration(10),
        proportions=(1, 2, 3, 4),
        main_permutation_order=(3, 1, 4, 2),
        permutation_index=(1, 1),
    )
    ft.add_layer()

    ft.add_layer(lambda node: node.get_fractal_order() > 1)
    ft.add_layer(lambda node: node.get_fractal_order() > 2)
    return ft

class FractalMusicalTreeChordFactory(TreeChordFactory):
    def update_chord_fractal_order(self):
        self._chord.add_words(str(self.get_musical_tree_node().get_fractal_order()), placement="below", relative_y=-10)


def create_test_fractal_relative_musical_tree():
    ft = FractalRelativeMusicTree(
        duration=TimelineDuration(10),
        proportions=(1, 2, 3, 4),
        main_permutation_order=(3, 1, 4, 2),
        permutation_index=(1, 1),
    )
    ft.add_layer()

    ft.add_layer(lambda node: node.get_fractal_order() > 1)
    ft.add_layer(lambda node: node.get_fractal_order() > 2)
    
    return ft


def create_test_timeline_tree():
    tlt = TimelineTree(duration=TimelineDuration(60))
    for d in [20, 10, 30]:
        tlt.add_child(TimelineTree(TimelineDuration(d)))
    for list_of_d, child in zip([[10, 2, 3, 5], [], [5, 20, 3, 2]], tlt.get_children()):
        for d in list_of_d:
            child.add_child(TimelineTree(TimelineDuration(d)))
    return tlt


class DemoValuedTree(ValuedTree):
    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = value

    def _check_child_to_be_added(self, child):
        if not isinstance(child, ValuedTree):
            raise TypeError
        else:
            return True

    def _set_value(self, value):
        self._value = Fraction(value)

    def get_value(self):
        return Fraction(self._value)


def create_test_valued_tree() -> DemoValuedTree:
    vt = DemoValuedTree.create_tree_from_list(test_fractal_structur_list, "value")
    # print(vt.get_tree_representation(key=lambda node: node.get_value()))

    """└── 10
    ├── 3
    │   ├── 3/5
    │   ├── 6/5
    │   │   ├── 6/25
    │   │   ├── 12/25
    │   │   ├── 3/25
    │   │   └── 9/25
    │   ├── 3/10
    │   └── 9/10
    │       ├── 27/100
    │       ├── 9/100
    │       ├── 9/25
    │       └── 9/50
    ├── 1
    ├── 4
    │   ├── 2/5
    │   ├── 4/5
    │   ├── 6/5
    │   │   ├── 6/25
    │   │   ├── 12/25
    │   │   ├── 3/25
    │   │   └── 9/25
    │   └── 8/5
    │       ├── 4/25
    │       ├── 8/25
    │       ├── 12/25
    │       └── 16/25
    └── 2
        ├── 4/5
        │   ├── 4/25
        │   ├── 8/25
        │   ├── 2/25
        │   └── 6/25
        ├── 3/5
        │   ├── 9/50
        │   ├── 3/50
        │   ├── 6/25
        │   └── 3/25
        ├── 2/5
        └── 1/5
    """
    return vt


def add_node_infos_to_graphic(vt, gt):
    for gn, vn in zip(gt.traverse(), vt.traverse()):
        value_label = gn.get_segment().start_mark_line.add_text_label(
            round(float(vn.get_value()), 1), font_size=8, bottom_margin=1
        )

        position_in_tree_label = gn.get_segment().start_mark_line.add_text_label(
            f"{vn.get_position_in_tree()}", font_size=8, placement="below", top_margin=1
        )
        if gn.get_distance() == 3:
            if vn.up.up.get_position_in_tree() == "4":
                if gn.up.get_children().index(gn) % 4 == 1:
                    position_in_tree_label.top_margin = 3
                    value_label.bottom_margin = 4
                elif gn.up.get_children().index(gn) % 4 == 2:
                    position_in_tree_label.top_margin = 5
                    value_label.bottom_margin = 7
                elif gn.up.get_children().index(gn) % 4 == 3:
                    position_in_tree_label.top_margin = 7
                    value_label.bottom_margin = 10
            else:
                if gn.up.get_children().index(gn) % 2 == 1:
                    position_in_tree_label.top_margin = 3
                    value_label.bottom_margin = 4
