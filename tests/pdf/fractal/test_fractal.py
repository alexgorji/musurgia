from pathlib import Path

from musurgia.fractaltree.fractaltree import FractalTree
from musurgia.pdf.line import HorizontalLineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.rowcolumn import DrawObjectColumn, DrawObjectRow
from musurgia.unittest import TestCase

path = Path(__file__)


def fractal_tree_to_column(fractal_tree, factor=1):
    c = DrawObjectColumn()
    c.add_draw_object(HorizontalLineSegment(length=fractal_tree.value * factor))
    fractal_tree.graphic = c
    if fractal_tree.get_children():
        r = DrawObjectRow()
        for child in fractal_tree.get_children():
            r.add_draw_object(fractal_tree_to_column(child, factor=factor))
        c.add_draw_object(r)

    return c


class TestFractal(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.ft = FractalTree(value=20)
        self.ft.add_layer()
        self.factor = 2
        fractal_tree_to_column(self.ft, self.factor)
        # self.ft_graphic = fractal_tree_to_column(self.ft, self.factor)

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
        l.bottom_margin = 4
        row = self.ft.graphic.draw_objects[1]
        row.top_margin = max([do.get_height() for do in row.draw_objects]) + 2
        with self.file_path(path, 'draw_with_text', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(10, 10)
            self.ft.graphic.draw(self.pdf)
            self.pdf.write(pdf_path)
