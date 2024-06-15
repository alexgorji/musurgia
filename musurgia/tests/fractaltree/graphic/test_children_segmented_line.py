from pathlib import Path

from musurgia.fractal.graphic import ChildrenSegmentedLine
from musurgia.pdf import Pdf, draw_ruler
from musurgia.tests.utils_for_tests import PdfTestCase
from musurgia.fractal.fractaltree import FractalTree

path = Path(__file__)


class TestChildrenSegmentedLine(PdfTestCase):
    def setUp(self):
        self.pdf = Pdf()
        self.fractal_tree = FractalTree(value=10, proportions=(1, 2, 3, 4), main_permutation_order=(3, 1, 4, 2),
                                        permutation_index=(1, 1))
        self.fractal_tree.add_layer()
        # self.fractal_tree.add_layer(lambda node: node.get_fractal_order() > 1)
        # self.fractal_tree.add_layer(lambda node: node.get_fractal_order() > 2)

    def test_children_segmented_line_root(self):
        chsl = ChildrenSegmentedLine([self.fractal_tree])
        assert len(chsl.segments) == 1

    def test_children_segmented_line_first_layer(self):
        chsl = ChildrenSegmentedLine(fractal_tree_children=self.fractal_tree.get_children(), unit=10,
                                     mark_line_length=6,
                                     shrink_factor=0.7)
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(10, 10)
            chsl.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)