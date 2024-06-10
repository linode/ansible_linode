"""Documentation fragments for the child_account_info module"""

result_child_account_samples = ['''{
    "active_since": "2018-01-01T00:01:01",
    "address_1": "123 Main Street",
    "address_2": "Suite A",
    "balance": 200,
    "balance_uninvoiced": 145,
    "billing_source": "external",
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
}''']


specdoc_examples = ['''
- name: Get info about a Child Account by EUUID
  linode.cloud.child_account_info:
    euuid: "FFFFFFFF-FFFF-FFFF-FFFFFFFFFFFFFFFF"''']
