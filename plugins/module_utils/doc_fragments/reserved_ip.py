"""Documentation fragments for the reserved_ip module"""

specdoc_examples = [
    """
- name: Reserve an IP in us-east
  linode.cloud.reserved_ip:
    region: us-east
    state: present
  register: reserved_ip""",
    """
- name: Reserve an IP with tags
  linode.cloud.reserved_ip:
    region: us-east
    tags:
      - lb
      - prod
    state: present""",
    """
- name: Unreserve (delete) a reserved IP
  linode.cloud.reserved_ip:
    address: "192.0.2.141"
    state: absent""",
]

result_reserved_ip_samples = [
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
