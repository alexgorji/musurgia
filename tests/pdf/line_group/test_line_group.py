
from pathlib import Path

from musurgia.pdf.drawobjectgroup import DrawObjectGroup
from musurgia.pdf.segmentedline import LineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.unittest import create_path, TestCase

path = Path(__file__)


def make_line_group():
    lg = DrawObjectGroup(inner_distance=7, bottom_margin=30)
    lg.add_draw_object(LineSegment(length=10))
    lg.add_draw_object(LineSegment(length=10))
    lg.add_draw_object(LineSegment(length=10))
    return lg


class Test(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_1(self):
        pdf = self.pdf
        pdf_path = create_path(path, 'test_1.pdf')
        lg = DrawObjectGroup(inner_distance=7)
        lg.add_draw_object(LineSegment(length=10))
        lg.add_draw_object(LineSegment(length=10))
        lg.add_draw_object(LineSegment(length=10))

        lg.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)

    def test_2(self):
        pdf = self.pdf
        pdf_path = create_path(path, 'test_2.pdf')

        lg = make_line_group()
        lg.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)

    def test_3(self):

        pdf = self.pdf
        pdf_path = create_path(path, 'test_3.pdf')
        lg = make_line_group()
        lg.draw(pdf)

        lg = make_line_group()
        lg.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)

    def test_4(self):

        pdf = self.pdf
        pdf_path = create_path(path, 'test_4.pdf')
        lg = make_line_group()
        lg.draw(pdf)

        lg = make_line_group()
        lg.relative_x = 50
        lg.relative_y = 50
        lg.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)

    def test_5a(self):
        pdf = self.pdf
        pdf_path = create_path(path, 'test_5a.pdf')
        line = LineSegment(length=10)
        line.draw_with_break(pdf)

        line = LineSegment(length=10)
        line.relative_x = 300
        line.draw_with_break(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)

    def test_5(self):

        pdf = self.pdf
        pdf_path = create_path(path, 'test_5.pdf')
        lg = make_line_group()
        lg.draw_with_break(pdf)

        lg = make_line_group()
        lg.relative_x = 300
        lg.draw_with_break(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)

    def test_6(self):

        pdf = self.pdf
        pdf_path = create_path(path, 'test_6.pdf')
        lg = make_line_group()
        lg.draw_with_break(pdf)

        lg = make_line_group()
        lg.relative_x = 300
        lg.relative_y = 240
        lg.draw_with_break(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)
