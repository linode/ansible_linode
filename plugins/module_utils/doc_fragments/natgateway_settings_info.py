"""Documentation fragments for the natgateway_settings_info module"""

specdoc_examples = ['''
- name: Get info about the current NAT Gateway settings
  linode.cloud.natgateway_settings_info: {}''']

result_natgateway_settings_samples = ['''{
  "allowed_ports_per_interface": [
    4096,
    8192,
    16384
  ],
  "maximum_autoscaling_addresses_per_natgateway": 100,
  "maximum_reserved_addresses_per_natgateway": 100
}''']
