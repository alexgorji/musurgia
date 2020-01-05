from unittest import TestCase

from testfilecontent import TestFileContent

tfc = TestFileContent()


class Test(TestCase):
    def test_1_1(self):
        with self.assertRaises(ValueError):
            tfc.assertTemplate('test_1')

    def test_1_2(self):
        tfc.assertTemplate('test_1.txt')

    def test_2_1(self):
        with self.assertRaises(AssertionError):
            tfc.assertTemplate('test_2.txt')

    def test_2_2(self):
        tfc.assertTemplate('test_2.txt', 'test_1_template.txt')
