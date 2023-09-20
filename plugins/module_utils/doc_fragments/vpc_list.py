"""Documentation fragments for the vpc_list module"""

specdoc_examples = ['''
- name: List all of the VPCs for the current user
  linode.cloud.vpc_list: {}''', '''
- name: List all of the VPCS for the current user with the given label
  linode.cloud.vpc_list:
    filters:
      - name: label
        values: my-vpc''']

result_vpc_samples = ['''[
    {
        "created": "2023-08-31T18:35:01",
        "description": "A description of this VPC",
        "id": 344,
        "label": "my-vpc",
        "region": "us-east",
        "subnets": [],
        "updated": "2023-08-31T18:35:03"
    }
]''']
