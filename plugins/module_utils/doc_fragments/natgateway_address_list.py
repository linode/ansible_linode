"""Documentation fragments for the natgateway_address_list module"""

specdoc_examples = ['''
- name: List the addresses for a NAT Gateway
  linode.cloud.natgateway_address_list:
    id: 123''']

result_natgateway_addresses_samples = ['''[
    {
      "address": "203.0.113.43",
      "in_use": true,
      "interface_count": 6,
      "portset_assignments": 6,
      "portset_capacity": 63
    },
    {
      "address": "203.0.113.44",
      "in_use": false,
      "interface_count": 0,
      "portset_assignments": 0,
      "portset_capacity": 63
    }
  ]''']
