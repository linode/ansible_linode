"""Documentation fragments for the vpc module"""

specdoc_examples = ['''
- name: Create a VPC 
  linode.cloud.vpc:
    label: my-vpc
    region: us-east
    description: A description of this VPC.
    state: present''',
'''
# NOTE: IPv6 VPCs may not currently be available to all users.
- name: Create a VPC with an auto-allocated IPv6 range
  linode.cloud.vpc:
    label: my-vpc
    region: us-east
    ipv6:
    - range: auto
    state: present''',
'''
- name: Delete a VPC
  linode.cloud.vpc:
    label: my-vpc
    state: absent''']

result_vpc_samples = ['''{
    "created": "2023-08-31T18:35:01",
    "description": "A description of this VPC",
    "id": 344,
    "ipv6": [
        {
            "range": "2001:db8:acad:0::/52"
        }
    ],
    "label": "my-vpc",
    "region": "us-east",
    "subnets": [],
    "updated": "2023-08-31T18:35:03"
}''']
