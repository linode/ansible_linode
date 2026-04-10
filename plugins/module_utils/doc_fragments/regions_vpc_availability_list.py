"""Documentation fragments for the regions_vpc_availability_list module"""

specdoc_examples = ['''
- name: List all of the Linode regions VPC availability
  linode.cloud.regions_vpc_availability_list: {}''']

result_regions_vpc_availability_samples = ['''[
    {
        "region": "nl-ams",
        "available": true,
        "available_ipv6_prefix_lengths": [
            48,
            52
        ]
    },
    {
        "region": "fr-par-2",
        "available": true,
        "available_ipv6_prefix_lengths": [
            48,
            52
        ]
    },
    {
        "region": "jp-tyo-3",
        "available": true,
        "available_ipv6_prefix_lengths": [
            48,
            52
        ]
    }
]''']
