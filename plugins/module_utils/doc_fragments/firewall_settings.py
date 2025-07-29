"""Documentation fragments for the firewall_settings module"""

specdoc_examples = ['''
- name: Update the default firewall settings
  linode.cloud.firewall_settings:
    default_firewall_ids:
      linode: 123456
      nodebalancer: 123456
      public_interface: 123456
      vpc_interface: 123456'''
]

result_firewall_settings_samples = ['''{
  "default_firewall_ids": {
    "linode": 123456,
    "nodebalancer": 123456,
    "public_interface": 123456,
    "vpc_interface": 123456
  }
}''']
