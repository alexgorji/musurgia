from pathlib import Path

from musurgia.fractal import FractalTree
from musurgia.fractal.fractaltree import FractalTreeNodeSegment
from musurgia.pdf import DrawObjectRow, DrawObjectColumn, Pdf, draw_ruler
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestCreateGraphic(PdfTestCase):
    def setUp(self):
        self.fractal_tree = FractalTree(value=10, proportions=(1, 2, 3, 4), main_permutation_order=(3, 1, 4, 2),
                                        permutation_index=(1, 1))
        self.fractal_tree.add_layer()
        self.fractal_tree.add_layer(lambda node: node.get_fractal_order() > 1)
        self.fractal_tree.add_layer(lambda node: node.get_fractal_order() > 2)

    def test_line_segment(self):
        assert self.fractal_tree.get_node_segment().unit == 1
        segment = self.fractal_tree.get_node_segment()
        assert isinstance(segment, FractalTreeNodeSegment)
        assert segment.length == self.fractal_tree.get_value()
        with self.assertRaises(AttributeError):
            segment.length = 10
        assert segment.start_mark_line.length == segment.end_mark_line.length == 3
        segment.unit = 10
        assert self.fractal_tree.get_node_segment().unit == 10
        assert segment.length == self.fractal_tree.get_value() * 10
        assert segment.start_mark_line.show
        assert not segment.end_mark_line.show
        segment.end_mark_line.show = True

        segment.start_mark_line.add_text_label('something')
        copied_segment = segment.__copy__()
        assert isinstance(copied_segment, FractalTreeNodeSegment)
        assert copied_segment.unit == segment.unit
        assert copied_segment.length == self.fractal_tree.get_value() * 10
        assert copied_segment.start_mark_line.show
        assert segment.end_mark_line.show
        copied_segment.unit = 5
        assert segment.unit == 10
        copied_segment.end_mark_line.show = False
        assert segment.end_mark_line.show
        assert not copied_segment.end_mark_line.show
        assert copied_segment.start_mark_line.get_text_labels()[0].value == 'something'

    def test_create_graphic_types(self):
        graphic = self.fractal_tree.create_graphic()
        assert isinstance(graphic, DrawObjectColumn)
        assert len(graphic.get_draw_objects()) == 2
        for do in graphic.get_draw_objects():
            assert isinstance(do, DrawObjectRow)
        row_1 = graphic.get_draw_objects()[0]
        row_2 = graphic.get_draw_objects()[1]
        assert len(row_1.get_draw_objects()) == 1
        assert isinstance(row_1.get_draw_objects()[0], FractalTreeNodeSegment)
        assert len(row_2.get_draw_objects()) == 4
        for do in row_2.get_draw_objects():
            assert isinstance(do, DrawObjectColumn)
        # segment is copied
        assert row_1.get_draw_objects()[0] != self.fractal_tree.get_node_segment()

    def test_create_graphic(self):
        for node in self.fractal_tree.traverse():
            node.get_node_segment().unit = 2
            if node.get_distance() < 3:
                node.get_node_segment().start_mark_line.add_text_label(f'{node.get_fractal_order()}', font_size=6)
        graphic = self.fractal_tree.create_graphic(unit=10)

        # for index, do in enumerate(graphic.traverse()):
        #     if isinstance(do, FractalTreeNodeSegment):
        #         do.straight_line.add_text_label(f's: {index}', font_size=5)
        #     elif isinstance(do, DrawObjectRow):
        #         do.add_text_label(f'r: {index}', font_size=5, placement='below', top_margin=2)
        #     else:
        #         do.add_text_label(f'c: {index}', font_size=5, placement='below', top_margin=4)
        pdf = Pdf()
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            pdf.translate_page_margins()
            draw_ruler(pdf, 'h')
            draw_ruler(pdf, 'v')
            pdf.translate(10, 10)
            graphic.draw(pdf)
            pdf.write_to_path(pdf_path)
