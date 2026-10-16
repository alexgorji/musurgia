import os
import unittest
from pathlib import Path
from types import TracebackType

from musurgia.tests.helpers.utils_for_tests import create_test_path

__all__ = ["XMLTestCase"]


class XMLTestCase(unittest.TestCase):
    def __init__(self, *args: str, **kwargs: str) -> None:
        super().__init__(*args, **kwargs)

    def _compare_contents(
        self,
        actual_file_path: Path,
        expected_file_path: Path,
    ) -> None:
        with open(actual_file_path, "r") as myfile:
            result = myfile.read()

        with open(expected_file_path, "r") as myfile:
            expected = myfile.read()

        self.assertEqual(expected, result)

    def assertCompareFiles(
        self,
        actual_file_path: Path,
        expected_file_path: Path | None = None,
    ) -> None:
        file_name, extension = os.path.splitext(actual_file_path)
        if not expected_file_path:
            if not extension:
                expected_file_path = Path(file_name + "_expected.xml")
            else:
                expected_file_path = Path(f"{file_name}_expected{extension}")

        self._compare_contents(actual_file_path, expected_file_path)

    def file_path(self, parent_path: Path, name: str) -> "FilePath":
        tfp = FilePath(self, parent_path, name, "xml")
        return tfp


class FilePath:
    def __init__(
        self, unittest: XMLTestCase, parent_path: Path, name: str, extension: str
    ) -> None:
        self._unittest: XMLTestCase | None = None
        self._parent_path: Path | None = None

        self.unittest = unittest
        self.parent_path = parent_path
        self.name = name
        self.extension = extension
        self.out_path: Path | None = None

    @property
    def unittest(self) -> XMLTestCase | None:
        return self._unittest

    @unittest.setter
    def unittest(self, val: XMLTestCase) -> None:
        self._unittest = val

    @property
    def parent_path(self) -> Path | None:
        return self._parent_path

    @parent_path.setter
    def parent_path(self, val: Path) -> None:
        self._parent_path = val

    def __enter__(self) -> Path:
        if not (self.parent_path):
            raise TypeError
        self.out_path = create_test_path(
            self.parent_path, self.name + "." + self.extension
        )
        return self.out_path

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if not (self.unittest and self.out_path):
            raise TypeError
        self.unittest.assertCompareFiles(self.out_path)
