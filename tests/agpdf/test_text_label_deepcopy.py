import os
from unittest import TestCase

from musurgia.agpdf.pdf import Pdf
from musurgia.agpdf.textlabel import Text
from musurgia.testcomparefiles import TestCompareFiles

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_1(self):
        pdf_path = path + '_test_1.pdf'
        tl = Text('test_1')
        tl.relative_x = 30
        copied = tl.__deepcopy__()
        copied.draw(self.pdf)
        self.pdf.write(pdf_path)
        TestCompareFiles().assertTemplate(file_path=pdf_path)
