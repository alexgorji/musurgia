import copy
from pathlib import Path
from unittest import skip

from musurgia.pdf.line import HorizontalLineSegment, VerticalSegmentedLine, VerticalLineSegment, StraightLine
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.pdf_tools import draw_ruler
from musurgia.pdf.rowcolumn import DrawObjectRow, DrawObjectColumn
from musurgia.pdf.labeled import TextLabel
from musurgia.tests.utils_for_tests import PdfTestCase

path = Path(__file__)


class TestRowColumnSimpleLines(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf(orientation='l')
        self.h_lines = [StraightLine(length=l, mode='h') for l in range(5, 20, 5)]
        self.v_lines = [StraightLine(length=l, mode='v') for l in range(5, 20, 5)]

    def test_simple_lines_row(self):
        row = DrawObjectRow(show_margins=True, show_borders=True)
        row.margins = (10, 10, 10, 10)
        for l in self.h_lines + self.v_lines:
            row.add_draw_object(l)

        for l in self.h_lines + self.v_lines:
            copied = copy.deepcopy(l)
            copied.top_margin = 10
            copied.left_margin = 10
            row.add_draw_object(copied)
        self.v_lines[-1].right_margin = 10

        with self.file_path(path, 'simple_lines_row', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.translate(10, 10)
            row.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)


class TestRowColumn(PdfTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf(orientation='l')
        self.row = self._make_row()
        self.column = self._make_column()

    def _make_row(self):
        r = DrawObjectRow()
        r.add_draw_object(HorizontalLineSegment(10))
        do2 = r.add_draw_object(HorizontalLineSegment(20))
        r.add_draw_object(VerticalSegmentedLine(lengths=[5, 6, 7, 8]))
        do2.start_mark_line.length = 6
        r.add_text_label(TextLabel('row', placement='left'))
        return r
        # print(self.row.get_draw_objects())

    def _make_column(self):
        c = DrawObjectColumn()
        c.add_draw_object(HorizontalLineSegment(10))
        do2 = c.add_draw_object(HorizontalLineSegment(20))
        c.add_draw_object(VerticalSegmentedLine(lengths=[5, 6, 7, 8]))
        do2.start_mark_line.length = 6
        return c

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
        draw_object_rows = [DrawObjectRow(show_segments=True, show_margins=True) for _ in range(4)]
        line_segments = [HorizontalLineSegment(l) for l in [30, 10, 20]]
        line_segments[-1].end_mark_line.show = True
        line_segments[-1].right_margin = 10
        for l in line_segments:
            draw_object_rows[0].add_draw_object(l)

        for i, l in enumerate(line_segments):
            copied = copy.deepcopy(l)
            copied.start_mark_line.length *= (i + 1)
            draw_object_rows[1].add_draw_object(copied)
            if i == len(line_segments) - 1:
                copied.end_mark_line.length += copied.start_mark_line.length
            copied.right_margin = 10

        for i, l in enumerate(line_segments):
            copied = copy.deepcopy(l)
            copied.start_mark_line.length *= (i + 1)
            draw_object_rows[2].add_draw_object(copied)
            if i == len(line_segments) - 1:
                copied.end_mark_line.length += copied.start_mark_line.length

        for i, l in enumerate(line_segments):
            copied = copy.deepcopy(l)
            copied.start_mark_line.length *= (i + 1)
            draw_object_rows[3].add_draw_object(copied)
            if i == len(line_segments) - 1:
                copied.end_mark_line.length += copied.start_mark_line.length
            copied.set_straight_line_relative_y(1.5)

        with self.file_path(path, 'draw_row_of_segments', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            for l in line_segments:
                copied = copy.deepcopy(l)
                copied.draw(self.pdf)
                self.pdf.translate(50, 0)

            self.pdf.reset_position()
            self.pdf.translate_page_margins()
            self.pdf.translate(0, 30)
            for i, l in enumerate(line_segments):
                copied = copy.deepcopy(l)
                copied.start_mark_line.length *= (i + 1)
                copied.draw(self.pdf)
                self.pdf.translate(50, 0)

            self.pdf.reset_position()
            self.pdf.translate_page_margins()
            self.pdf.translate(0, 60)
            for i, l in enumerate(line_segments):
                copied = copy.deepcopy(l)
                copied.start_mark_line.length *= (i + 1)
                copied.relative_y -= (i * 3)
                copied.start_mark_line.add_text_label(str(copied.relative_y), font_size=8)
                copied.start_mark_line.add_text_label(str(copied.start_mark_line.length), font_size=8, placement='left')
                copied.straight_line.add_text_label(str(copied.straight_line.length), font_size=8, placement='below',
                                                    left_margin=5, top_margin=2)
                copied.draw(self.pdf)
                self.pdf.translate(50, 0)

            self.pdf.reset_position()
            self.pdf.translate_page_margins()
            self.pdf.translate(0, 90)
            for do in draw_object_rows:
                do.draw(self.pdf)
                self.pdf.translate(0, 20)

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

    def test_travers_column(self):
        c = DrawObjectColumn()
        r = DrawObjectRow()
        c.add_draw_object(r)
        c_1 = c.add_draw_object(HorizontalLineSegment(length=10))
        r_1 = r.add_draw_object(HorizontalLineSegment(length=20))
        assert list(c.traverse()) == [c, r, r_1, c_1]

    def test_travers_row(self):
        r = DrawObjectRow()
        c = DrawObjectColumn()
        cc = DrawObjectColumn()

        r.add_draw_object(c)
        r_1 = r.add_draw_object(HorizontalLineSegment(length=10))
        r.add_draw_object(cc)
        rr = DrawObjectRow()
        c.add_draw_object(rr)
        rr_1 = rr.add_draw_object(HorizontalLineSegment(length=10))
        c_1 = c.add_draw_object(HorizontalLineSegment(length=10))
        cc_1 = cc.add_draw_object(HorizontalLineSegment(length=10))
        cc_2 = cc.add_draw_object(HorizontalLineSegment(length=10))
        assert list(r.traverse()) == [r, c, rr, rr_1, c_1, r_1, cc, cc_1, cc_2]

    @skip
    def test_row_column_borders_and_labels(self):
        def add_text_labels(do):
            if isinstance(do, HorizontalLineSegment):
                do = do.start_mark_line
            do.add_text_label(label=TextLabel('below label', placement='below'))
            do.add_text_label(label=TextLabel(f'rel_x: {round(do.relative_x)}', placement='below'))
            do.add_text_label(label=TextLabel(f'rel_x2: {round(do.get_relative_x2())}', placement='below'))
            do.add_text_label(label=TextLabel('above label', placement='above'))
            do.add_text_label(label=TextLabel(f'rel_y: {round(do.relative_y)}', placement='above'))
            do.add_text_label(label=TextLabel(f'rel_y2: {round(do.get_relative_y2())}', placement='above'))
            do.add_text_label(label=TextLabel(f'left label', placement='left'))
            do.add_text_label(label=TextLabel(f'left label', placement='left'))
            do.add_text_label(label=TextLabel(f'left label', placement='left'))
            for tl in do.get_text_labels():
                tl.font_size = 8

        hls = HorizontalLineSegment(length=20)
        hls.start_mark_line.length = 10

        vls = VerticalLineSegment(length=15)
        vls.start_mark_line.length = vls.end_mark_line.length = 10

        control_hls = copy.deepcopy(hls)
        control_hls.top_margin = 10
        control_hls.left_margin = 20
        control_hls.bottom_margin = 20

        add_text_labels(control_hls)

        r = DrawObjectRow(show_borders=True, show_margins=True)
        first_hls = copy.deepcopy(hls)
        first_hls.left_margin = 5
        second_hls = copy.deepcopy(hls)
        second_hls.start_mark_line.length *= 0.5
        second_hls.end_mark_line.show = True

        r.add_draw_object(first_hls)
        r.add_draw_object(second_hls)

        first_vls = copy.deepcopy(vls)
        second_vls = copy.deepcopy(vls)

        second_vls.end_mark_line.show = first_vls.end_mark_line.show = True
        first_vls.left_margin = 10
        first_vls.right_margin = 5
        r.add_draw_object(first_vls)
        r.add_draw_object(second_vls)

        r.top_margin = 10
        r.left_margin = 20
        r.bottom_margin = 20

        add_text_labels(r)

        c = DrawObjectColumn(show_borders=True)
        first_hls = copy.deepcopy(hls)
        second_hls = copy.deepcopy(hls)
        first_hls.bottom_margin = 10
        c.add_draw_object(first_hls)
        c.add_draw_object(second_hls)
        c.top_margin = 10
        c.left_margin = 20

        add_text_labels(c)

        main_column = DrawObjectColumn()
        main_column.add_draw_object(control_hls)
        main_column.add_draw_object(r)
        main_column.add_draw_object(c)

        with self.file_path(path, 'borders_and_labels', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, mode='v')
            draw_ruler(self.pdf, mode='h')
            main_column.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
