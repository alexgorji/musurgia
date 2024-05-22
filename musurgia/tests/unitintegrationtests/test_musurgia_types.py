from unittest import TestCase

from musurgia.musurgia_types import check_type, \
    MusurgiaTypeError, check_matrix_index_values, check_permutation_order_values, create_error_message


class TestCreateErrorMessage(TestCase):

    def test_check_create_message_errors(self):
        with self.assertRaises(AttributeError):
            create_error_message(v=3, t=list, function_name='function_name')
        with self.assertRaises(AttributeError):
            create_error_message(v=3, t=list, function_name='function_name', class_name='ClassName')
        with self.assertRaises(AttributeError):
            create_error_message(v=3, t=list, function_name='function_name', property_name='property_name')
        with self.assertRaises(AttributeError):
            create_error_message(v=3, t=list, function_name='function_name', method_name='method_name')
        with self.assertRaises(AttributeError):
            create_error_message(v=3, t=list, class_name='ClassName')
        with self.assertRaises(AttributeError):
            create_error_message(v=3, t=list, class_name='ClassName', argument_name='argument_name')
        with self.assertRaises(AttributeError):
            create_error_message(v=3, t=list, class_name='ClassName', method_name='method_name')
        with self.assertRaises(AttributeError):
            create_error_message(v=3, t=list, class_name='ClassName', property_name='property_name',
                                 argument_name='argument_name')
        with self.assertRaises(AttributeError):
            create_error_message(v=3, t=list, method_name='method_name')
        with self.assertRaises(AttributeError):
            create_error_message(v=3, t=list, property_name='property_name')
        with self.assertRaises(AttributeError):
            create_error_message(v=3, t=list, property_name='argument_name')
        with self.assertRaises(AttributeError):
            create_error_message(v=3, t=list, message='message')
        with self.assertRaises(AttributeError):
            create_error_message(v=3, message='message')
        with self.assertRaises(AttributeError):
            create_error_message(t=list, message='message')
        with self.assertRaises(AttributeError):
            create_error_message()

    def test_check_create_message(self):
        assert create_error_message(v=3, t=list) == 'Value 3 must be of type list not int'
        assert create_error_message(v=3, t=list, function_name='function_name',
                                    argument_name='argument_name') == 'function_name:argument_name: Value 3 must be of type list not int'
        assert create_error_message(v=3, t=list, class_name='ClassName', method_name='method_name',
                                    argument_name='argument_name') == 'ClassName.method_name:argument_name: Value 3 must be of type list not int'
        assert create_error_message(v=3, t=list, class_name='ClassName',
                                    property_name='property_name') == 'ClassName.property_name: Value 3 must be of type list not int'
        assert create_error_message(class_name='ClassName',
                                    property_name='property_name',
                                    message=f'Value {3} must be greater than 5') == 'ClassName.property_name: Value 3 must be greater than 5'


class TestCheckTypeFunction(TestCase):

    def test_matrix_data(self):
        assert check_type([], 'MatrixData')
        assert check_type([[1, 2, 3]], 'MatrixData')
        assert check_type([[1, 2, 3], [4, 5, 6]], 'MatrixData')

        with self.assertRaises(MusurgiaTypeError):
            check_type(0, 'MatrixData')
        with self.assertRaises(MusurgiaTypeError):
            check_type([1, 2, 3], 'MatrixData')
        with self.assertRaises(MusurgiaTypeError):
            check_type([[1, 2, 3], [1, 2]], 'MatrixData')

    def test_matrix_index(self):
        # wrong type
        with self.assertRaises(TypeError):
            check_type([1, 2], 'MatrixIndex')
        with self.assertRaises(TypeError):
            check_type((-1, 2), 'MatrixIndex')
        # wrong lengths
        with self.assertRaises(TypeError):
            check_type((1, 2, 3), 'MatrixIndex')
        with self.assertRaises(TypeError):
            check_type(1, 'MatrixIndex')
        with self.assertRaises(TypeError):
            check_type((1,), 'MatrixIndex')

    def test_non_negative_integer(self):
        assert check_type(2, 'NonNegativeInteger')
        assert check_type(0, 'NonNegativeInteger')

        with self.assertRaises(MusurgiaTypeError):
            check_type(-2, 'NonNegativeInteger')

        with self.assertRaises(MusurgiaTypeError):
            check_type(1.2, 'NonNegativeInteger')

    def test_permutation_order(self):
        assert check_type((2, 3, 1), 'PermutationOrder')

        with self.assertRaises(MusurgiaTypeError):
            assert check_type([2, 2], 'PermutationOrder')
        with self.assertRaises(MusurgiaTypeError):
            assert check_type((2, 2), 'PermutationOrder')
        with self.assertRaises(MusurgiaTypeError):
            assert check_type((1, 3, 4), 'PermutationOrder')
        with self.assertRaises(MusurgiaTypeError):
            assert check_type((2, 3, 4), 'PermutationOrder')
        with self.assertRaises(MusurgiaTypeError):
            assert check_type((1, 3, 4, 2, 4), 'PermutationOrder')

    def test_positive_integer(self):
        assert check_type(2, 'PositiveInteger')

        with self.assertRaises(MusurgiaTypeError):
            check_type(-2, 'PositiveInteger')

        with self.assertRaises(MusurgiaTypeError):
            check_type(0, 'PositiveInteger')

        with self.assertRaises(MusurgiaTypeError):
            check_type(-1, 'PositiveInteger')

        with self.assertRaises(MusurgiaTypeError):
            check_type(1.2, 'PositiveInteger')

    def test_matrix_transpose_type(self):
        assert check_type('regular', 'MatrixTransposeMode')
        assert check_type('diagonal', 'MatrixTransposeMode')
        with self.assertRaises(MusurgiaTypeError):
            assert check_type('wrong', 'MatrixTransposeMode')


class TestCheckValues(TestCase):

    def test_matrix_index(self):
        # wrong index
        with self.assertRaises(ValueError):
            check_matrix_index_values(index=(2, 3), number_of_rows=3, number_of_columns=2)
        with self.assertRaises(ValueError):
            check_matrix_index_values(index=(4, 2), number_of_rows=3, number_of_columns=2)

        assert check_matrix_index_values(index=(2, 3), number_of_rows=3, number_of_columns=4)

    def test_permutation_order(self):
        assert check_permutation_order_values((4, 3, 1, 2), size=4)
        with self.assertRaises(ValueError):
            assert check_permutation_order_values((4, 3, 1, 2), size=5)
        with self.assertRaises(ValueError):
            assert check_permutation_order_values((4, 3, 1, 2), size=3)
