"""Documentation fragments for the nodebalancer_vpc_list module"""

specdoc_examples = ['''
- name: List all of the Nodebalancer VPC configurations for a specific NodeBalancer
  linode.cloud.nodebalancer_vpc_list:
    nodebalancer_id: 123''']

result_nodebalancer_vpcs_samples = ['''[
  {
      "id": 123,
      "nodebalancer_id": 456,
      "vpc_id": 89,
      "subnet_id": 21,
      "ipv4_range": "10.0.0.3/32",
      "ipv6_range": null,
      "purpose": "frontend"
  },
  {
      "id": 124,
      "nodebalancer_id": 457,
      "vpc_id": 90,
      "subnet_id": 22,
      "ipv4_range": "10.0.0.4/30",
      "ipv6_range": "/64",
      "purpose": "backend"
  }
],''']
