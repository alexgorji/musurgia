import os
import unittest
from diff_pdf_visually import pdf_similar  # type: ignore
from musurgia.tests.helpers.utils_for_tests import FilePath
from musurgia.pdf.labeled import (
    TextLabel,
)
from musurgia.pdf.line import (
    StraightLine,
)
from musurgia.pdf.rowcolumn import (
    DrawObjectColumn,
)

from musurgia.pdf.drawobject import MasterDrawObject

__all__ = [
    "PdfTestCase",
]


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


numbers = ["one", "two", "three"]


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


def add_test_above_labels(drawobject):
    for t in numbers:
        drawobject.add_text_label(f"above label {t}", placement="above", font_size=8)


def add_test_below_labels(drawobject):
    for t in numbers:
        drawobject.add_text_label(f"below label {t}", placement="below", font_size=8)


def add_test_left_labels(drawobject):
    for t in numbers:
        drawobject.add_text_label(f"left label {t}", placement="left", font_size=8)


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


# def add_test_right_labels(drawobject):
#     for t in numbers:
#         drawobject.add_text_label(f'right label {t}', placement='right', font_size=8)


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
