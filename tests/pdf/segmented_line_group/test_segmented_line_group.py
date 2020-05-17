from pathlib import Path

from musurgia.pdf.drawobjectgroup import DrawObjectGroup
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.segmentedline import SegmentedLine
from musurgia.pdf.textlabel import TextLabel
from musurgia.unittest import TestCase, create_test_path

path = Path(__file__)


class Test(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf(orientation='l')

    def test_get_height(self):
        slg = DrawObjectGroup(inner_distance=7, relative_y=10)
        slg.add_draw_object(SegmentedLine(5 * [10]))
        slg.add_draw_object(SegmentedLine(5 * [10]))
        slg.add_draw_object(SegmentedLine(5 * [10]))
        expected = slg.get_height()
        actual = 23
        self.assertEqual(expected, actual)

    def test_get_relative_y2(self):
        slg = DrawObjectGroup(inner_distance=7, relative_y=10)
        slg.add_draw_object(SegmentedLine(5 * [10]))
        slg.add_draw_object(SegmentedLine(5 * [10]))
        slg.add_draw_object(SegmentedLine(5 * [10]))
        expected = slg.get_relative_y2()
        actual = 33
        self.assertEqual(expected, actual)

    def test_draw(self):
        pdf_path = create_test_path(path, 'draw.pdf')
        slg = DrawObjectGroup(inner_distance=17)
        sl_1 = slg.add_draw_object(SegmentedLine([5, 10, 15, 20]))
        sl_2 = slg.add_draw_object(SegmentedLine([20, 10, 5, 30]))
        sl_1.add_text_label(TextLabel('no.1'))
        sl_2.add_text_label(TextLabel('no.2'))
        slg.draw(self.pdf)
        self.pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)

    def test_break(self):
        pdf_path = create_test_path(path, 'break.pdf')
        self.pdf.l_margin = 10
        slg = DrawObjectGroup(inner_distance=10, bottom_margin=20)
        sl_1 = slg.add_draw_object(SegmentedLine(50 * [10]))
        sl_2 = slg.add_draw_object(SegmentedLine(50 * [10]))
        sl_1.name = 'I'
        sl_2.name = 'II'
        sl_1.name.relative_x = -5
        sl_2.name.relative_x = -5
        slg.draw(self.pdf)
        self.pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)

    def test_break_with_one_line(self):
        pdf_path = create_test_path(path, 'break_with_one_line.pdf')
        self.pdf.l_margin = 10
        slg = DrawObjectGroup(inner_distance=10, bottom_margin=20)
        sl_1 = slg.add_draw_object(SegmentedLine(50 * [10]))
        sl_1.name = 'I'
        sl_1.name.relative_x = -5
        slg.draw(self.pdf)
        self.pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)

    def test_page_break(self):
        pdf_path = create_test_path(path, 'page_break.pdf')
        self.pdf.l_margin = 10
        slg = DrawObjectGroup(inner_distance=10, bottom_margin=20)
        sl_1 = slg.add_draw_object(SegmentedLine(200 * [10]))
        sl_2 = slg.add_draw_object(SegmentedLine(200 * [10]))
        sl_1.name = 'I'
        sl_2.name = 'II'
        sl_1.name.relative_x = -5
        sl_2.name.relative_x = -5
        slg.draw(self.pdf)
        self.pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)
