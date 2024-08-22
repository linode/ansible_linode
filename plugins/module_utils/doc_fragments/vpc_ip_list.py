"""Documentation fragments for the vpc_ip_list module"""

specdoc_examples = ["""
- name: List all IPs of a specific VPC.
  linode.cloud.vpc_ip_list:
    vpc_id: 12345""",
]

result_vpc_ip_view_samples = [
    """[
    {
        "address": "10.0.0.2",
        "address_range": null,
        "vpc_id": 56242,
        "subnet_id": 55829,
        "region": "us-mia",
        "linode_id": 57328104,
        "config_id": 60480976,
        "interface_id": 1373818,
        "active": false,
        "nat_1_1": null,
        "gateway": "10.0.0.1",
        "prefix": 24,
        "subnet_mask": "255.255.255.0"
    }
]"""
]
