import unittest
from unittest.mock import patch
from ansible_collections.linode.cloud.plugins.modules.account_info import Module


class TestAccountInfoModule(unittest.TestCase):

    def setUp(self):
        self.module = Module()

    def test_exec_module(self):
        expected_account_data = {
            "active_promotions": [
                {
                    "credit_monthly_cap": "10.00",
                    "credit_remaining": "50.00",
                    "description": "Receive up to $10 off your services every month for 6 months! Unused credits will expire once this promotion period ends.",
                    "expire_dt": "2018-01-31T23:59:59",
                    "image_url": "https://linode.com/10_a_month_promotion.svg",
                    "service_type": "all",
                    "summary": "$10 off your Linode a month!",
                    "this_month_credit_remaining": "10.00"
                }
            ],
            "active_since": "2018-01-01T00:01:01",
            "address_1": "123 Main Street",
            "address_2": "Suite A",
            "balance": 200,
            "balance_uninvoiced": 145,
            "billing_source": "akamai",
            "capabilities": [
                "Linodes",
                "NodeBalancers",
                "Block Storage",
                "Object Storage"
            ],
            "city": "Philadelphia",
            "company": "Linode LLC",
            "country": "US",
            "credit_card": {
                "expiry": "11/2022",
                "last_four": 1111
            },
            "email": "john.smith@linode.com",
            "euuid": "E1AF5EEC-526F-487D-B317EBEB34C87D71",
            "first_name": "John",
            "last_name": "Smith",
            "phone": "215-555-1212",
            "state": "PA",
            "tax_id": "ATU99999999",
            "zip": "19102-1234"
        }

        # Call the exec_module method
        result = self.module.exec_module()

        # Check if the result contains the 'account' key
        self.assertIn("account", result)

        # Check if the 'account' value matches the expected data
        self.assertEqual(result["account"], expected_account_data)

if __name__ == '__main__':
    unittest.main()

