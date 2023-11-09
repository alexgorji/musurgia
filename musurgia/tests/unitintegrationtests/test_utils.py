from unittest import TestCase

from musurgia.utils import MusurgiaTypeError, check_type


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
