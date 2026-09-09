"""Documentation fragments for the region_vpc_availability_info module"""

result_vpc_availability_samples = ["""
{
  "region": "us-east",
  "available": true,
  "available_ipv6_prefix_lengths": [52]
}
"""]


specdoc_examples = ["""
- name: Get info about VPC availability for a region
  linode.cloud.region_vpc_availability_info:
    region: us-east
"""]
