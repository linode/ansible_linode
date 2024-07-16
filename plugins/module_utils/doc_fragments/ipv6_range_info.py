"""Documentation fragments for the ipv6_range_info module"""

specdoc_examples = ['''
- name: Get info about an IPv6 range
  linode.cloud.ipv6_range_info:
    range: "2600:3c01::"''']


result_range_samples = ['''{
  "is_bgp": false,
  "linodes": [
    123
  ],
  "prefix": 64,
  "range": "2600:3c01::",
  "region": "us-east"
}''']
