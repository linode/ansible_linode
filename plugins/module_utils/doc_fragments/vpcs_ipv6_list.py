"""Documentation fragments for the vpcs_ipv6_list module"""

specdoc_examples = ["""
- name: List all IPv6 addresses for the current user.
  linode.cloud.vpcs_ipv6_list: {}""",
]

result_addresses_samples = [
    """[
  {
    "active": false,
    "address": null,
    "address_range": null,
    "config_id": 123,
    "database_id": null,
    "gateway": null,
    "interface_id": 123,
    "ipv6_addresses": [
      {
        "slaac_address": "2001:db8:acad:1:abcd:ef12:3456:7890"
      }
    ],
    "ipv6_is_public": false,
    "ipv6_range": "2001:db8:acad:1::/64",
    "linode_id": 123,
    "nat_1_1": "",
    "nodebalancer_id": null,
    "prefix": 64,
    "region": "us-mia",
    "subnet_id": 123,
    "subnet_mask": "",
    "vpc_id": 123
  },
  {
    "active": false,
    "address": null,
    "address_range": null,
    "config_id": 123,
    "database_id": null,
    "gateway": null,
    "interface_id": 123,
    "ipv6_addresses": [],
    "ipv6_is_public": false,
    "ipv6_range": "2001:db8::/64",
    "linode_id": 123,
    "nat_1_1": "",
    "nodebalancer_id": null,
    "prefix": 64,
    "region": "us-mia",
    "subnet_id": 271170,
    "subnet_mask": "",
    "vpc_id": 262108
  },
  {
    "active": false,
    "address": null,
    "address_range": null,
    "config_id": 123,
    "database_id": null,
    "gateway": null,
    "interface_id": 123,
    "ipv6_addresses": [],
    "ipv6_is_public": false,
    "ipv6_range": "2001:db8::/64",
    "linode_id": 123,
    "nat_1_1": "",
    "nodebalancer_id": null,
    "prefix": 64,
    "region": "us-mia",
    "subnet_id": 123,
    "subnet_mask": "",
    "vpc_id": 123
  }
]"""
]
