import os
from unittest import TestCase

from musurgia.testcomparefiles import TestCompareFiles

tfc = TestCompareFiles()

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def test_1_1(self):
        with self.assertRaises(ValueError):
            wrong_path = path + '_test_1'
            tfc.assertTemplate(wrong_path)

    def test_1_2(self):
        file_path = path + '_test_1.txt'
        tfc.assertTemplate(file_path)

    def test_2_1(self):
        file_path = path + '_test_2.txt'
        with self.assertRaises(AssertionError):
            tfc.assertTemplate(file_path)

    def test_2_2(self):
        file_path = path + '_test_2.txt'
        template_path= path + '_test_1_template.txt'
        tfc.assertTemplate(file_path=file_path, template_path=template_path)
