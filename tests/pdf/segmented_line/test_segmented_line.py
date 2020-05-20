from pathlib import Path

from musurgia.pdf.pdf import Pdf
from musurgia.pdf.segmentedline import SegmentedLine
from musurgia.pdf.text import TextLabel
from musurgia.unittest import TestCase, create_test_path

path = Path(__file__)


class Test(TestCase):
    def test_draw(self):
        pdf_path = create_test_path(path, 'draw.pdf')
        sl = SegmentedLine(lengths=[1, 3, 2, 5], factor=5)
        pdf = Pdf(orientation='portrait')
        sl.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(pdf_path)

    def test_break(self):
        pdf_path = create_test_path(path, 'break.pdf')
        sl = SegmentedLine(lengths=30 * [20])
        sl.bottom_margin = 35
        pdf = Pdf(orientation='portrait')
        sl.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_page_break(self):
        pdf_path = create_test_path(path, 'page_break.pdf')
        sl = SegmentedLine(lengths=200 * [20])
        sl.bottom_margin = 35
        pdf = Pdf(orientation='portrait')
        sl.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_text_label(self):
        pdf_path = create_test_path(path, 'text_label.pdf')
        sl = SegmentedLine(lengths=30 * [10])
        sl.add_text_label(TextLabel('bla is bla'))
        pdf = Pdf(orientation='portrait')
        sl.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_name(self):
        pdf_path = create_test_path(path, 'name.pdf')
        sl = SegmentedLine(lengths=30 * [10], name='vla')
        pdf = Pdf(orientation='portrait')
        sl.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)
