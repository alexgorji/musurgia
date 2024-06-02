from pathlib import Path

from musurgia.fractal.fractaltree import FractalTree
from musurgia.pdf.line import HorizontalRuler
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.pdf.rowcolumn import DrawObjectColumn
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


def make_ft():
    ft = FractalTree(value=20, proportions=(1, 2, 3), main_permutation_order=(3, 1, 2), permutation_index=(1, 1))
    ft.add_layer()
    ft.get_children()[0].add_layer()
    ft.get_children()[-1].add_layer()
    return ft


class TestFractalTreeGraphic(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf(orientation='l')

    def test_draw_clipped(self):
        unit = 20
        ft = make_ft()
        ft.graphic.unit = unit
        c = DrawObjectColumn()

        c.bottom_margin = 50
        ruler = HorizontalRuler(unit=unit, length=ft.graphic.get_width(), bottom_margin=5)
        c.add_draw_object(ruler)
        c.add_draw_object(ft.graphic)
        self.pdf.r_margin = self.pdf.l_margin = ((self.pdf.w - 13 * unit) / 2)
        self.pdf.translate_page_margins()
        c.clipped_draw(self.pdf)
        with self.file_path(path, 'draw_clipped', 'pdf') as pdf_path:
            self.pdf.write_to_path(pdf_path)

    def test_draw(self):
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            ft = make_ft()
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(10, 10)
            ft.graphic.unit = 2
            ft.graphic.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_add_labels(self):
        def generate_ruler():
            ruler_length = self.pdf.w - self.pdf.l_margin - self.pdf.r_margin
            ruler = HorizontalRuler(length=ruler_length, unit=3, show_first_label=True, label_show_interval=5)
            for segment in ruler.segments:
                try:
                    segment.start_mark_line.get_text_labels()[0].font_size = 8
                except IndexError:
                    pass
            return ruler

        with self.file_path(path, 'add_labels', 'pdf') as pdf_path:
            ft = make_ft()
            self.pdf.translate_page_margins()

            ruler = generate_ruler()
            ruler.draw(self.pdf)
            self.pdf.translate(0, 10)
            ft.graphic.unit = 3
            ft.graphic.add_labels(lambda node: node.get_fractal_order() if node.get_fractal_order() is not None else '',
                                  font_size=8, bottom_margin=3)
            ft.graphic.add_labels(lambda node: round(float(node.get_value()), 2), placement='below', font_size=6,
                                  top_margin=2)
            ft.graphic.change_segment_attributes(bottom_margin=5)

            ft.graphic.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
