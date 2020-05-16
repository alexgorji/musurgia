
from pathlib import Path

from musurgia.pdf.drawobjectgroup import DrawObjectGroup
from musurgia.pdf.segmentedline import LineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.unittest import create_path, TestCase

path = Path(__file__)


def make_line_group():
    lg = DrawObjectGroup(inner_distance=10, bottom_margin=20)
    lg.add_draw_object(LineSegment(length=10))
    lg.add_draw_object(LineSegment(length=10))
    lg.add_draw_object(LineSegment(length=10))
    return lg


class Test(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_inner_distance(self):
        pdf = self.pdf
        pdf_path = create_path(path, 'inner_distance.pdf')
        lg = make_line_group()
        lg.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)

    def test_bottom_margin(self):
        pdf = self.pdf
        pdf_path = create_path(path, 'bottom_margin.pdf')
        lg = make_line_group()
        lg.draw(pdf)
        new_lg = make_line_group()
        new_lg.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)

    def test_change_inner_distance(self):
        pdf = self.pdf
        pdf_path = create_path(path, 'change_inner_distance.pdf')
        lg = make_line_group()
        lg.draw(pdf)
        new_lg = make_line_group()
        new_lg.inner_distance = 15
        new_lg.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)

    def test_change_position(self):
        pdf = self.pdf
        pdf_path = create_path(path, 'change_position.pdf')
        lg = make_line_group()
        lg.draw(pdf)

        lg = make_line_group()
        lg.relative_x = 10
        lg.relative_y = 10
        lg.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)

    def test_draw_with_line_break(self):

        pdf = self.pdf
        pdf_path = create_path(path, 'draw_with_line_break.pdf')
        lg = make_line_group()
        lg.draw(pdf)

        lg = make_line_group()
        lg.relative_x = 300
        lg.draw_with_break(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)

    def test_page_break(self):
        pdf = self.pdf
        pdf_path = create_path(path, 'page_break.pdf')
        lg = make_line_group()
        lg.draw(pdf)
        lg = make_line_group()
        lg.relative_x = 300
        lg.relative_y = 240
        lg.draw_with_break(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)
