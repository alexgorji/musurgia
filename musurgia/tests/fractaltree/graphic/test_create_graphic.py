import copy
from pathlib import Path

from musurgia.fractal import FractalTree
from musurgia.fractal.fractaltree import FractalTreeNodeSegment
from musurgia.pdf import DrawObjectRow, DrawObjectColumn, Pdf, draw_ruler, HorizontalRuler
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
        copied_segment = copy.deepcopy(segment)
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

    def test_set_node_value(self):
        seg = FractalTreeNodeSegment(node_value=10)
        assert seg.length == 10
        assert seg.get_node_value() == 10
        seg.set_node_value(20)
        assert seg.get_node_value() == 20
        assert seg.length == 20
        seg.unit = 2
        assert seg.get_node_value() == 20
        assert seg.length == 40
        seg.set_node_value(10)
        assert seg.get_node_value() == 10
        assert seg.length == 20

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
            if node.get_distance() == 1:
                node.get_node_segment().start_mark_line.add_text_label(f'value:{round(node.get_value(), 2)}',
                                                                       font_size=8,
                                                                       bottom_margin=1)
                node.get_node_segment().top_margin = 3
            if node.get_distance() < 3:
                node.get_node_segment().start_mark_line.add_text_label(f'{node.get_fractal_order()}', font_size=6,
                                                                       bottom_margin=1)
                node.get_node_segment().start_mark_line.add_text_label(f'{node.get_position_in_tree()}', font_size=4,
                                                                       bottom_margin=1)
        unit = 15
        graphic = self.fractal_tree.create_graphic(unit=unit)

        pdf = Pdf()
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            pdf.translate_page_margins()
            draw_ruler(pdf, 'h', unit=unit, first_label=-1)
            draw_ruler(pdf, 'v', unit=10)
            pdf.translate(unit, 10)
            graphic.draw(pdf)
            pdf.write_to_path(pdf_path)

    def test_draw_clipped(self):
        self.fractal_tree.change_value(50)
        for node in self.fractal_tree.traverse():
            if node.get_distance() == 1:
                node.get_node_segment().start_mark_line.add_text_label(f'value:{round(node.get_value(), 2)}',
                                                                       font_size=12,
                                                                       bottom_margin=1)
                node.get_node_segment().top_margin = 3
            node.get_node_segment().start_mark_line.add_text_label(f'{node.get_fractal_order()}', font_size=10,
                                                                   bottom_margin=1)
            node.get_node_segment().start_mark_line.add_text_label(f'{node.get_position_in_tree()}', font_size=8,
                                                                   bottom_margin=1)
            if node.get_position_in_tree() == '4.1.4':
                node.get_node_segment().start_mark_line.get_above_text_labels()[-1].left_margin = 3
            elif node.get_position_in_tree() == '4.2.3':
                node.get_node_segment().start_mark_line.get_above_text_labels()[-1].left_margin = 5

        unit = 20
        graphic = self.fractal_tree.create_graphic(unit=unit, distance=10)
        graphic.top_margin = 10
        pdf = Pdf(orientation='l')

        c = DrawObjectColumn()
        c.bottom_margin = 20
        ruler = HorizontalRuler(unit=unit, length=graphic.get_width(), bottom_margin=5)
        c.add_draw_object(ruler)
        c.add_draw_object(graphic)
        pdf.r_margin = pdf.l_margin = ((pdf.w - 13 * unit) / 2)
        pdf.translate_page_margins()
        c.clipped_draw(pdf)
        with self.file_path(path, 'draw_clipped', 'pdf') as pdf_path:
            pdf.write_to_path(pdf_path)
