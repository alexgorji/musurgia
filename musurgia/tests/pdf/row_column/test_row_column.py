from pathlib import Path

from musurgia.pdf.line import HorizontalLineSegment, VerticalSegmentedLine
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.pdf.rowcolumn import DrawObjectRow, DrawObjectColumn
from musurgia.pdf.labeled import TextLabel
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestRowColumn(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf(orientation='l')
        self._make_row()
        self._make_column()

    def _make_row(self):
        r = DrawObjectRow()
        r.add_draw_object(HorizontalLineSegment(10))
        do2 = r.add_draw_object(HorizontalLineSegment(20))
        r.add_draw_object(VerticalSegmentedLine(lengths=[5, 6, 7, 8]))
        do2.start_mark_line.length = 6
        self.row = r

    def _make_column(self):
        c = DrawObjectColumn()
        c.add_draw_object(HorizontalLineSegment(10))
        do2 = c.add_draw_object(HorizontalLineSegment(20))
        c.add_draw_object(VerticalSegmentedLine(lengths=[5, 6, 7, 8]))
        do2.start_mark_line.length = 6
        self.column = c

    def test_draw_row(self):
        self.pdf.translate_page_margins()
        draw_ruler(self.pdf, 'h')
        draw_ruler(self.pdf, 'v')
        self.pdf.translate(10, 10)
        r = self.row
        r.add_text_label(label=TextLabel('below label', placement='below'))

        r.draw(self.pdf)

        with self.file_path(path, 'draw_row', 'pdf') as pdf_path:
            self.pdf.write_to_path(pdf_path)

    def test_wrong_add_draw_object(self):
        r = DrawObjectRow()
        with self.assertRaises(TypeError):
            r.add_draw_object('something')

    def test_draw_row_of_segments(self):
        r = DrawObjectRow()
        r.add_draw_object(HorizontalLineSegment(30))
        r.add_draw_object(HorizontalLineSegment(10))
        r.add_draw_object(HorizontalLineSegment(20))
        with self.file_path(path, 'draw_row_of_segments', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(10, 10)
            r.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_draw_column_of_row_of_segments(self):
        r = DrawObjectRow()
        r.add_draw_object(HorizontalLineSegment(30))
        r.add_draw_object(HorizontalLineSegment(10))
        r.add_draw_object(HorizontalLineSegment(20))
        c = DrawObjectColumn()
        c.add_draw_object(HorizontalLineSegment(60))
        c.add_draw_object(r)

        with self.file_path(path, 'draw_column_of_row_of_segments', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(10, 10)
            c.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_draw_row_of_column_of_segments(self):
        c = DrawObjectColumn()
        c.add_draw_object(HorizontalLineSegment(30))
        c.add_draw_object(HorizontalLineSegment(10))
        c.add_draw_object(HorizontalLineSegment(20))
        r = DrawObjectRow()
        r.add_draw_object(c)

        with self.file_path(path, 'draw_row_of_column_of_segments', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h')
            draw_ruler(self.pdf, 'v')
            self.pdf.translate(10, 10)
            c.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_draw_column(self):
        self.pdf.translate_page_margins()
        draw_ruler(self.pdf, 'h')
        draw_ruler(self.pdf, 'v')
        self.pdf.translate(10, 10)
        c = self.column
        c.add_text_label(TextLabel('below label', placement='below', top_margin=3))
        c.draw(self.pdf)
        with self.file_path(path, 'draw_column', 'pdf') as pdf_path:
            self.pdf.write_to_path(pdf_path)
