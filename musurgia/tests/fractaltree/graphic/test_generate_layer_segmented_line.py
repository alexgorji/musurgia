from pathlib import Path

from musurgia.fractal.fractaltree import FractalTree
from musurgia.pdf.line import HorizontalRuler
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.pdf.rowcolumn import DrawObjectColumn
from musurgia.pdf.text import PageText
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


def make_ft():
    ft = FractalTree(value=20, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
    ft.add_layer()
    ft.get_children()[0].add_layer()
    ft.get_children()[-1].add_layer()
    return ft


def change_layer_graphic(layer_graphic):
    for segment in layer_graphic.segments:
        segment.straight_line.add_label(round(float(segment.node.get_value()), 2), font_size=6, bottom_margin=3)


def change_ft_graphic(ft, unit):
    ft.graphic.set_unit(unit)
    ft.graphic.add_labels(lambda node: round(float(node.get_value()), 2), placement='above', font_size=6,
                          bottom_margin=2, left_margin=0.5)
    ft.graphic.add_labels(lambda node: node.get_fractal_order(), placement='below', font_size=6, top_margin=1,
                          left_margin=0.5)

    ft.graphic.change_segment_attributes(bottom_margin=5)


class TestGenerateLayerSegmentedLine(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf(orientation='l')

    def test_draw_with_clipping(self):
        ft = make_ft()
        unit = 20
        change_ft_graphic(ft, unit)

        c = DrawObjectColumn()
        c.bottom_margin = 20
        ruler = HorizontalRuler(unit=unit, length=ft.graphic.get_width(), bottom_margin=10)
        c.add_draw_object(ruler)

        c.add_draw_object(ft.graphic)

        segmented_line = ft.graphic.generate_layer_segmented_line(layer_number=2)
        change_layer_graphic(segmented_line)
        segmented_line.segments[0].start_mark_line.add_text_label('blabla', placement='left', right_margin=1)

        c.add_draw_object(segmented_line)

        self.pdf.r_margin = self.pdf.l_margin = ((self.pdf.w - 13 * unit) / 2)
        self.pdf.translate_page_margins()

        c.clipped_draw(self.pdf)
        with self.file_path(path, 'draw_clipped', 'pdf') as pdf_path:
            self.pdf.write_to_path(pdf_path)

    def test_draw(self):
        unit = 10
        ft = make_ft()
        self.pdf.translate_page_margins()
        draw_ruler(self.pdf, 'h', first_label=-1, unit=unit)
        draw_ruler(self.pdf, 'v')

        self.pdf.translate(10, 20)

        change_ft_graphic(ft, unit)
        ft.graphic.draw(self.pdf)

        self.pdf.translate(0, ft.graphic.get_height() + 10)

        segmented_line = ft.graphic.generate_layer_segmented_line(layer_number=2)
        change_layer_graphic(segmented_line)
        segmented_line.segments[0].start_mark_line.add_text_label('blabla', placement='left', right_margin=1)
        segmented_line.draw(self.pdf)
        pt = PageText('Some Title', h_position='center', font_weight='bold', font_size=12, top_margin=10,
                      left_margin=10)
        pt.draw(self.pdf)
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            self.pdf.write_to_path(pdf_path)
