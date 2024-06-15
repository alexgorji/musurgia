from pathlib import Path

from musurgia.fractal import FractalTree
from musurgia.fractal.graphic import GraphicTree
from musurgia.pdf import DrawObjectColumn, DrawObjectRow, Pdf, draw_ruler
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


def create_test_fractal_tree():
    ft = FractalTree(value=10, proportions=(1, 2, 3, 4), main_permutation_order=(3, 1, 4, 2),
                     permutation_index=(1, 1))
    ft.add_layer()

    ft.add_layer(lambda node: node.get_fractal_order() > 1)
    ft.add_layer(lambda node: node.get_fractal_order() > 2)
    return ft


class TestGraphicTree(PdfTestCase):
    def setUp(self):
        self.ft = create_test_fractal_tree()
        self.gt = GraphicTree(self.ft)
        self.pdf = Pdf()

    def test_populate(self):
        traversed_ft = list(self.ft.traverse())
        traversed_gt = list(self.gt.traverse())
        assert len(traversed_ft) == len(traversed_gt)
        for fnode, gnode in zip(traversed_ft, traversed_gt):
            assert gnode.get_node_segment().length == float(fnode.get_value() * self.gt.unit)

    def test_graphic(self):
        for node in self.gt.traverse():
            assert isinstance(node.get_graphic(), DrawObjectColumn)
            if node.is_leaf:
                number_draw_objects = 1
            else:
                number_draw_objects = 2
            assert len(node.get_graphic().get_draw_objects()) == number_draw_objects
            assert node.get_graphic().get_draw_objects()[0] == node.get_node_segment()
            if not node.is_leaf:
                assert isinstance(node.get_graphic().get_draw_objects()[1], DrawObjectRow)
                for ch, do in zip(node.get_children(), node.get_graphic().get_draw_objects()[1].get_draw_objects()):
                    assert isinstance(do, DrawObjectColumn)
                    assert do.get_draw_objects()[0] == ch.get_node_segment()

    def test_end_mark_lines(self):
        self.gt._show_last_mark_lines()
        for node in self.gt.traverse():
            if node.is_last_child:
                assert node.get_node_segment().end_mark_line.show is True
            else:
                assert node.get_node_segment().end_mark_line.show is False

    # def test_add_distance(self):
    #     self.gt._add_distance()

    def test_draw_graphic(self):
        unit = 10
        self.gt.unit = unit

        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h', unit=unit, first_label=-1)
            draw_ruler(self.pdf, 'v', unit=10)
            self.pdf.translate(unit, 10)
            self.gt.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
