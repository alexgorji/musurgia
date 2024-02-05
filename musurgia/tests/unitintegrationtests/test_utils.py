from unittest import TestCase

from musurgia.utils import MusurgiaTypeError, check_type

import os
import unittest
from pathlib import Path

from diff_pdf_visually import pdf_similar


class TestErrors(TestCase):
    def test_musurgia_type_error(self):
        with self.assertRaises(TypeError):
            MusurgiaTypeError()
        with self.assertRaises(TypeError):
            MusurgiaTypeError(t='myType')
        with self.assertRaises(TypeError):
            MusurgiaTypeError(v=3)

        self.assertEqual(MusurgiaTypeError(t='myType', v=3).msg, "3 must be of type myType not <class 'int'>.")
        self.assertEqual(MusurgiaTypeError(t='myType', v=3, argument_name='arg1').msg,
                         "Value of arg1=3 must be of type myType not <class 'int'>.")
        self.assertEqual(MusurgiaTypeError(t='myType', v=3, argument_name='arg1', method_name='get_arg1').msg,
                         "get_arg1: Value of arg1=3 must be of type myType not <class 'int'>.")
        self.assertEqual(
            MusurgiaTypeError(t='myType', v=3, argument_name='arg1', method_name='get_arg1', obj=object).msg,
            "<class 'object'>.get_arg1: Value of arg1=3 must be of type myType not <class "
            "'int'>.")


class TestCheckType(TestCase):
    def test_checktype_non_negative_int(self):
        check_type(t='non_negative_int', v=3)
        with self.assertRaises(MusurgiaTypeError):
            check_type(t='non_negative_int', v='3')


def create_test_path(path, test_name):
    return path.parent.joinpath(f'{path.stem}_{test_name}')


class TestFilePath:
    def __init__(self, unittest, parent_path, name, extension):
        self._unittest = None
        self._parent_path = None
        # self._name = None
        # self._extension = None

        self.unittest = unittest
        self.parent_path = parent_path
        self.name = name
        self.extension = extension
        self.out_path = None

    @property
    def unittest(self):
        return self._unittest

    @unittest.setter
    def unittest(self, val):
        if not isinstance(val, TestCase):
            raise TypeError(f"unittest.value must be of type {type(TestCase)} not{type(val)}")
        self._unittest = val

    @property
    def parent_path(self):
        return self._parent_path

    @parent_path.setter
    def parent_path(self, val):
        if not isinstance(val, Path):
            raise TypeError(f"parent_path.value must be of type {type(Path)} not{type(val)}")
        self._parent_path = val

    def __enter__(self):
        self.out_path = create_test_path(self.parent_path, self.name + '.' + self.extension)
        return self.out_path

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unittest.assertCompareFiles(self.out_path)


class TestCase(unittest.TestCase):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _compare_pdfs(self, actual_file_path, expected_file_path, verbosity):
        self.assertTrue(pdf_similar(actual_file_path, expected_file_path, verbosity=verbosity))

    def _compare_contents(self, actual_file_path, expected_file_path):
        with open(actual_file_path, 'r') as myfile:
            result = myfile.read()

        with open(expected_file_path, 'r') as myfile:
            expected = myfile.read()

        self.assertEqual(expected, result)

    def assertCompareFiles(self, actual_file_path, expected_file_path=None, verbosity=0):
        file_name, extension = os.path.splitext(actual_file_path)
        if not expected_file_path:
            if not extension:
                raise ValueError('actual_file_path has no file extension')
            expected_file_path = file_name + '_expected' + extension

        if extension == '.pdf':
            self._compare_pdfs(actual_file_path, expected_file_path, verbosity=verbosity)
        else:
            self._compare_contents(actual_file_path, expected_file_path)

    def file_path(self, parent_path, name, extension):
        tfp = TestFilePath(self, parent_path, name, extension)
        return tfp
