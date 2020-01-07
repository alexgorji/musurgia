import os
from unittest import TestCase

from musurgia.testcomparefiles import TestCompareFiles

tfc = TestCompareFiles()
path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def test_1(self):
        file_path = path + '_a1.pdf'
        template_path = path + '_a2.pdf'
        tfc.assertTemplate(file_path, template_path)

    def test_2(self):
        with self.assertRaises(AssertionError):
            file_path = path + '_a1.pdf'
            template_path = path + '_b.pdf'
            tfc.assertTemplate(file_path, template_path)
