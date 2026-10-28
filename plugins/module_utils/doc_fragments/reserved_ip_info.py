"""Documentation fragments for the reserved_ip_info module"""

specdoc_examples = [
    """
- name: Get info about a reserved IP address
  linode.cloud.reserved_ip_info:
    address: "192.0.2.141"
  register: ip_info"""
]

reserved_ip_info_response_sample = [
    """{
  "address": "192.0.2.141",
  "assigned_entity": null,
  "gateway": "192.0.2.1",
  "interface_id": null,
  "linode_id": null,
  "prefix": 24,
  "public": true,
  "rdns": "",
  "region": "us-east",
  "reserved": true,
  "subnet_mask": "255.255.255.0",
  "tags": [
    "lb",
    "prod"
  ],
  "type": "ipv4",
  "vpc_nat_1_1": null
}"""
]
