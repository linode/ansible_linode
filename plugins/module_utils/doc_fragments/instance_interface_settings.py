"""Documentation fragments for the instance module"""

specdoc_examples = ['''
- name: Configure the interface settings of a Linode Instance
  linode.cloud.instance_interface_settings:
    linode_id: 123
    network_helper: true
    default_route:
        ipv4_interface_id: 123
        ipv6_interface_id: 456
'''
]

result_samples = ['''
{
  "default_route": {
    "ipv4_eligible_interface_ids": [
      123,
      456
    ],
    "ipv4_interface_id": 456,
    "ipv6_eligible_interface_ids": [
      123
    ],
    "ipv6_interface_id": 123
  },
  "network_helper": true
}
''']
