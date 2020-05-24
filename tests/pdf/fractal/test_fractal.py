from pathlib import Path

from musurgia.fractaltree.fractaltree import FractalTree
from musurgia.pdf.line import HorizontalLineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.rowcolumn import DrawObjectColumn, DrawObjectRow
from musurgia.unittest import TestCase

path = Path(__file__)


def fill_tree_with_columns(fractal_tree, factor=1):
    max_large_ml = 6
    min_large_ml = 3
    for node in fractal_tree.traverse():
        node.graphic = DrawObjectColumn()
        segment = node.graphic.add_draw_object(HorizontalLineSegment(length=node.value * factor))
        ml_length = (max_large_ml - (
                node.get_distance() * (max_large_ml - min_large_ml) / fractal_tree.number_of_layers)) / 2
        segment.start_mark_line.length = ml_length
        segment.end_mark_line.length = ml_length
        if node.get_children():
            node.children_graphics_row = node.graphic.add_draw_object(DrawObjectRow(top_margin=3))
        if node.up:
            node.up.children_graphics_row.add_draw_object(node.graphic)
        if not node.up or node.up.get_children().index(node) == len(node.up.get_children()) - 1:
            node.graphic.draw_objects[0].end_mark_line.show = True
            node.graphic.draw_objects[0].end_mark_line.length *= 2
        if not node.up or node.up.get_children().index(node) == 0:
            node.graphic.draw_objects[0].start_mark_line.length *= 2


class TestFractal(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf(orientation='l')
        self.ft = FractalTree(value=20)
        self.ft.add_layer()
        self.factor = 2
        # fractal_tree_to_column(self.ft, self.factor)
        # self.ft_graphic = fractal_tree_to_column(self.ft, self.factor)
        fill_tree_with_columns(self.ft, self.factor)

    def test_draw(self):
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(10, 10)
            self.ft.graphic.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_draw_with_text(self):
        leaf = self.ft.get_leaves()[1]
        leaf_start_mark_line = leaf.graphic.draw_objects[0].start_mark_line
        leaf_start_mark_line.add_label('bla')
        l = leaf_start_mark_line.add_label('blue')
        # l.bottom_margin = 2
        row = self.ft.graphic.draw_objects[1]
        row.top_margin = max(
            [do.draw_objects[0].start_mark_line.get_above_text_labels_height() for do in row.draw_objects])
        print(row.top_margin)
        with self.file_path(path, 'draw_with_text', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(10, 10)
            self.ft.graphic.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_draw_filled_tree(self):
        ft = FractalTree(value=20)
        ft.add_layer()
        ft.get_children()[1].add_layer()
        fill_tree_with_columns(ft, 2)
        # for node in ft.traverse():
        #     print(node.index)
        #     print(node.graphic.draw_objects)

        with self.file_path(path, 'draw_filled_tree', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(10, 10)
            ft.graphic.draw(self.pdf)
            self.pdf.write(pdf_path)
