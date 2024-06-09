from pathlib import Path

from musurgia.fractal import FractalTree
from musurgia.pdf import Pdf, draw_ruler, TextLabel, DrawObjectColumn
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestCreatLayerGraphic(PdfTestCase):
    def setUp(self):
        self.fractal_tree = FractalTree(value=10, proportions=(1, 2, 3, 4), main_permutation_order=(3, 1, 4, 2),
                                        permutation_index=(1, 1))
        self.fractal_tree.add_layer()
        self.fractal_tree.add_layer(lambda node: node.get_fractal_order() > 1)
        self.fractal_tree.add_layer(lambda node: node.get_fractal_order() > 2)
        for index, node in enumerate(self.fractal_tree.traverse()):
            text_label = TextLabel(node.get_position_in_tree(), font_size=8)
            if index % 2 == 1:
                text_label.placement = 'below'
                text_label.top_margin = 1
            else:
                text_label.bottom_margin = 3
            if node.get_distance() > 2:
                text_label.font_size = 6
            node.get_node_segment().straight_line.add_text_label(text_label)
            if node.get_position_in_tree() == '4.4':
                node.get_node_segment().straight_line.get_above_text_labels()[0].bottom_margin += 1
            if node.get_position_in_tree() == '4.2.1':
                node.get_node_segment().straight_line.get_below_text_labels()[0].top_margin += 1

    def test_create_layer_graphic(self):
        unit = 24
        graphic = self.fractal_tree.create_graphic(unit=unit, distance=12, shrink_factor=0.6)
        graphic.bottom_margin = 10

        graphic_layer_2 = self.fractal_tree.create_layer_graphic(layer_number=2, unit=unit, shrink_factor=0.6)
        # graphic_layer_2.get_draw_objects()[0].add_text_label(TextLabel(value='layer 2', placement='left', font_size=8))
        graphic_layer_2.bottom_margin = 10

        graphic_layer_3 = self.fractal_tree.create_layer_graphic(layer_number=3, unit=unit, shrink_factor=0.6)
        graphic_layer_3.add_text_label(TextLabel(value='layer 3', placement='left', font_size=8))

        c = DrawObjectColumn()

        c.add_draw_object(graphic)
        c.add_draw_object(graphic_layer_2)
        c.add_draw_object(graphic_layer_3)

        pdf = Pdf(orientation='l')
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            pdf.translate_page_margins()
            draw_ruler(pdf, 'h', unit=unit, first_label=-1)
            draw_ruler(pdf, 'v', unit=unit)
            pdf.translate(unit, 10)
            c.draw(pdf)
            pdf.write_to_path(pdf_path)
