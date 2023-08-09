import unittest

from linode_api4 import ApiError
from plugins.module_utils.linode_database_shared import validate_allow_list, validate_shared_db_input, call_protected_provisioning


class LinodeDatabaseSharedTest(unittest.TestCase):

    def test_validate_allow_list_valid_cidr(self):
        # Valid CIDR format
        allow_list = {"192.168.0.1/24", "10.0.0.0/16", "172.16.0.0/12"}
        self.assertIsNone(validate_allow_list(allow_list))

    def test_validate_allow_list_invalid_cidr(self):
        # Invalid CIDR format
        allow_list = {"192.168.0.1/24", "10.0.0.0", "172.16.0.0/12", "200.100.50.25"}
        with self.assertRaises(ValueError):
            validate_allow_list(allow_list)

    def test_validate_shared_db_input_with_allow_list(self):
        # Valid allow_list
        params = {"allow_list": {"192.168.0.1/24", "10.0.0.0/16"}}
        self.assertIsNone(validate_shared_db_input(params))

    def test_validate_shared_db_input_without_allow_list(self):
        # No allow_list present in params
        params = {"other_field": "value"}
        self.assertIsNone(validate_shared_db_input(params))

    def test_call_protected_provisioning_with_exception(self):
        # Simulate an ApiError with status 400
        def mock_provisioning_function():
            raise ApiError(status=400, message="Api Error")

        result = call_protected_provisioning(mock_provisioning_function)
        self.assertIsNone(result)

    def test_call_protected_provisioning_with_other_exception(self):
        # Simulate an ApiError with status other than 400
        def mock_provisioning_function():
            raise ApiError(status=404, message="Not found")

        with self.assertRaises(ApiError):
            call_protected_provisioning(mock_provisioning_function)
