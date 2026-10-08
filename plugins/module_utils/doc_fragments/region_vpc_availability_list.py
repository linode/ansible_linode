"""Documentation fragments for the region_vpc_availability_list module"""

specdoc_examples = [
    """
- name: List VPC availability for all regions.
  linode.cloud.region_vpc_availability_list: {}""",
]

result_vpc_availabilities_samples = ['''[
    {
      "region": "au-mel",
      "available": true,
      "available_ipv6_prefix_lengths": [52]
    },
    {
      "region": "nz-akl-1",
      "available": false,
      "available_ipv6_prefix_lengths": []
    }
]''']
