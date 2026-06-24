"""Documentation fragments for the vpc_default_ranges_info module"""

specdoc_examples = ['''
- name: Get info about the default and forbidden IPv4 address ranges for VPCs
  linode.cloud.vpc_default_ranges_info:
''']

result_samples = ['''
{
  "default_ipv4_ranges": [
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/17"
  ],
  "forbidden_ipv4_ranges": [
    "0.0.0.0/8",
    "10.64.12.199/24",
    "172.21.89.19/15",
    "192.168.128.0/17",
    "203.0.113.190/32"
  ]
}
''']
