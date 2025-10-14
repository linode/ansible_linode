"""Documentation fragments for the vpc module"""

specdoc_examples = ['''
- name: Create a VPC subnet
  linode.cloud.vpc_subnet:
    vpc_id: 12345
    label: my-subnet
    ipv4: '10.0.0.0/24'
    state: present''',
'''
# NOTE: IPv6 VPCs may not currently be available to all users.
- name: Create a VPC subnet with an auto-allocated IPv6 range
  linode.cloud.vpc_subnet:
    vpc_id: 12345
    label: my-subnet
    ipv6:
    - range: auto
    state: present''','''
- name: Delete a VPC Subnet
  linode.cloud.vpc_subnet:
    vpc_id: 12345
    label: my-subnet
    state: absent''']

result_subnet_samples = ['''{
    "created": "2023-08-31T18:53:04",
    "id": 271,
    "ipv4": "10.0.0.0/24",
    "ipv6": [
        {
            "range": "2001:db8:acad:300::/56"
        }
    ],
    "label": "test-subnet",
    "linodes": [
        {
            "id": 1234567,
            "interfaces": [{"active": false, "id": 654321}]
        }
    ],
    "databases": [
        {
            "id": 1234567,
            "ipv4_range": "10.0.0.16/28",
            "ipv6_range": "2001:db8:1234:1::/64"
        }
    ],
    "updated": "2023-08-31T18:53:04"
}''']
