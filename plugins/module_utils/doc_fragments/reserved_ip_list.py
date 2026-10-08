"""Documentation fragments for the reserved_ip_list module"""

reserved_ip_list_specdoc_examples = [
    """
- name: List all reserved IPs for the current Linode Account
  linode.cloud.reserved_ip_list: {}""",
    """
- name: List reserved IPs filtered by tag
  linode.cloud.reserved_ip_list:
    filters:
      - name: tags
        values:
          - lb"""
]

result_reserved_ip_list_samples = [
    """[
  {
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
  }
]"""
]
