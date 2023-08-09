import unittest
from plugins.module_utils.linode_helper import (
    dict_select_spec,
    filter_null_values,
    drop_empty_strings,
    validate_required,
)


class LinodeHelperTest(unittest.TestCase):

    def test_dict_select_spec(self):
        target = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3",
            "key4": "value4",
        }
        spec = {
            "key1": "some description",
            "key3": "another description",
            "key5": "extra description",  # This should be ignored in the result
        }
        expected_result = {
            "key1": "value1",
            "key3": "value3",
            "key5": None,
        }
        result = dict_select_spec(target, spec)
        self.assertEqual(result, expected_result)

    def test_filter_null_values(self):
        input_dict = {
            "key1": "value1",
            "key2": None,
            "key3": "value3",
            "key4": None,
            "key5": "",
            "key6": "value6",
        }
        expected_result = {
            "key1": "value1",
            "key3": "value3",
            "key5": "",
            "key6": "value6",
        }
        result = filter_null_values(input_dict)
        self.assertEqual(result, expected_result)

    def test_drop_empty_strings(self):
        input_dict = {
            "key1": "value1",
            "key2": None,
            "key3": "",
            "key4": "value4",
        }
        expected_result = {
            "key1": "value1",
            "key4": "value4",
        }
        result = drop_empty_strings(input_dict)
        self.assertEqual(result, expected_result)

    def test_validate_required_with_missing_fields(self):
        required_fields = {"field1", "field2", "field3"}
        params = {"field1": "value1", "field4": "value4"}
        with self.assertRaises(Exception) as context:
            validate_required(required_fields, params)

        exception_fields = str(context.exception)

        self.assertTrue("field2" in exception_fields and "field3" in exception_fields)

    def test_validate_required_with_all_fields(self):
        required_fields = {"field1", "field2", "field3"}
        params = {"field1": "value1", "field2": "value2", "field3": "value3"}
        try:
            validate_required(required_fields, params)
        except Exception as e:
            self.fail(f"validate_required raised an unexpected exception: {e}")



