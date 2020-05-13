from pathlib import Path

from musurgia.pdf.segmentedline import LineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.textlabel import TextLabel
from musurgia.unittest import TestCase, create_path

path = Path(__file__)


class Test(TestCase):
    def test_one_segment_with_factor(self):
        pdf_path = create_path(path, 'one_segment_with_factor.pdf')
        pdf = Pdf()
        line = LineSegment(length=20, relative_x=0, factor=5)
        line.end_mark_line.show = True
        line.draw(pdf=pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_one_segment_with_end_mark_line(self):
        pdf_path = create_path(path, 'one_segment_with_end_mark_line.pdf')
        pdf = Pdf()
        line = LineSegment(length=60, relative_x=70)
        line.end_mark_line.show = True
        line.draw(pdf=pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_one_segment_with_text_label(self):
        pdf_path = create_path(path, 'one_segment_with_text_label.pdf')
        pdf = Pdf()
        line = LineSegment(length=60, relative_x=70)
        line.end_mark_line.show = True
        line.add_text_label(TextLabel('bla', font_size=8))
        line.draw(pdf=pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_one_segment_with_multiple_text_labels(self):
        pdf_path = create_path(path, 'one_segment_with_multiple_text_labels.pdf')
        pdf = Pdf()
        line = LineSegment(length=60, relative_x=70)
        line.end_mark_line.show = True
        TextLabel.DEFAULT_FONT_SIZE = 8

        line.end_mark_line.add_text_label(TextLabel(3))
        line.end_mark_line.add_text_label(TextLabel(4, relative_y=-4))
        line.end_mark_line.add_text_label(TextLabel(5, relative_y=-6))
        line.add_text_label(TextLabel('bla'))
        line.add_text_label(TextLabel('bla bla', relative_y=-4))
        line.draw(pdf=pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)
        TextLabel.DEFAULT_FONT_SIZE = 10

    def test_two_consecutive_segments(self):
        pdf_path = create_path(path, 'two_consecutive_segments.pdf')
        pdf = Pdf()
        line_1 = LineSegment(length=10)
        line_2 = LineSegment(length=20, relative_x=10)
        line_2.end_mark_line.show = True
        line_1.draw(pdf)
        line_1.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_two_segments_with_break(self):
        pdf_path = create_path(path, 'two_segments_with_break.pdf')
        pdf = Pdf()
        line_1 = LineSegment(length=10, relative_x=20)
        line_2 = LineSegment(length=20, relative_x=210)
        line_2.end_mark_line.show = True
        line_1.draw_with_break(pdf)
        line_2.draw_with_break(pdf)
        pdf.write(pdf_path)

    def test_two_segments_with_different_y(self):
        pdf_path = create_path(path, 'two_segments_with_different_y.pdf')
        pdf = Pdf(orientation='landscape')
        line_1 = LineSegment(length=10)
        line_2 = LineSegment(length=20, relative_y=10)
        line_1.draw(pdf)
        line_2.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_bottom_margin(self):
        pdf_path = create_path(path, 'bottom_margin.pdf')
        pdf = Pdf(orientation='landscape')
        line_1 = LineSegment(length=10, bottom_margin=20)
        line_2 = LineSegment(length=20)
        line_1.draw(pdf)
        line_2.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)


