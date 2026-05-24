"""Documentation fragments for the region_vpc_availability_info module"""

specdoc_examples = ['''
- name: Get Info of a Linode Region VPC Availability
  linode.cloud.region_vpc_availability_info:
    api_version: v4beta
    id: us-mia''']

result_region_vpc_availability_samples = ['''{
    "region": "us-mia",
    "available": true,
    "available_ipv6_prefix_lengths": [
        48,
        52
    ]
}''']
