from unittest import TestCase
import os


class TestFileContent(TestCase):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def assertTemplate(self, file_path, template_path=None):
        if not template_path:
            file_name, extension = os.path.splitext(file_path)
            if not extension:
                raise ValueError('file_path has no file extension')
            template_path = file_name + '_template' + extension

        with open(file_path, 'r') as myfile:
            result = myfile.read()

        with open(template_path, 'r') as myfile:
            template = myfile.read()

        self.assertEqual(template, result)
