"""Documentation fragments for the vpc_list module"""

specdoc_examples = ['''
- name: List all of the subnets under a VPC
  linode.cloud.vpc_subnet_list:
    vpc_id: 12345
  ''', '''
- name: List all of the subnets with a given label under a VPC
  linode.cloud.vpc_subnet_list:
    vpc_id: 12345
    filters:
      - name: label
        values: my-subnet''']

result_vpc_samples = ['''[
    {
        "created": "2023-08-31T18:53:04",
        "id": 271,
        "ipv4": "10.0.0.0/24",
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
    }
]''']
