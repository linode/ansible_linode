"""Documentation fragments for the natgateway_address_info module"""

specdoc_examples = ['''
- name: Get info about a NAT Gateway Address
  linode.cloud.natgateway_address_info:
    id: 123
    address: 100.123.97.131 ''']

result_natgateway_address_samples = ['''{
  "address": "203.0.113.43",
  "in_use": true,
  "interface_count": 6,
  "portset_assignments": 6,
  "portset_capacity": 63
}''']
