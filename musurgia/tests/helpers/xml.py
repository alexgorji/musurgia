import os
import unittest

from musurgia.tests.helpers.utils_for_tests import (
    FilePath,
)


__all__ = ["XMLTestCase"]


class XMLTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _compare_contents(self, actual_file_path, expected_file_path):
        with open(actual_file_path, "r") as myfile:
            result = myfile.read()

        with open(expected_file_path, "r") as myfile:
            expected = myfile.read()

        self.assertEqual(expected, result)

    def assertCompareFiles(self, actual_file_path, expected_file_path=None):
        file_name, extension = os.path.splitext(actual_file_path)
        if not expected_file_path:
            if not extension:
                expected_file_path += ".xml"
            expected_file_path = file_name + "_expected" + ".xml"

        self._compare_contents(actual_file_path, expected_file_path)

    def file_path(self, parent_path, name):
        tfp = FilePath(self, parent_path, name, "xml")
        return tfp
