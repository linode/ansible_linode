"""Documentation fragments for the natgateway module"""

specdoc_examples = ['''
- name: Create a natgateway
  linode.cloud.natgateway:
    label: my-ng
    region: us-east
    addresses:
        - address: 203.0.113.42
        - address: 203.0.113.43
    default_ports_per_interface: 4096
    use_autoscaling: false
    vpc_subnet_id: 42
    state: present''', '''
- name: Update a NAT Gateway label
  linode.cloud.natgateway:
    id: 123
    label: my-ng-updated
    state: present''', '''
- name: Delete a NAT Gateway by label
  linode.cloud.natgateway:
    label: my-ng
    state: absent''', '''
- name: Delete a NAT Gateway by id
  linode.cloud.natgateway:
    id: 123
    state: absent
''']

result_natgateway_samples = ['''{
  "id": 123,
  "region": "us-east",
  "addresses": [
    { "address": "203.0.113.42" },
    { "address": "203.0.113.43" }
  ],
  "address_autoscale_max": 0,
  "default_ports_per_interface": 4096,
  "label": "my-ng",
  "portset_assignments": 0,
  "portset_capacity": 30,
  "vpc_subnet": {
    "id": 42,
    "type": "vpc_subnet",
    "label":"my-subnet",
    "url": "https://www.something.com/vpcs/42/subnets/41"
    "vpc_id": 13,
    "vpc_label": "my-vpc"
  },
  "created": "2026-01-01T00:01:01",
  "updated": "2026-03-01T00:01:01"
}
''']

result_addresses_samples = ['''[
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
