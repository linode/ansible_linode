"""Documentation fragments for the vpc module"""

specdoc_examples = ['''
- name: Create a VPC 
  linode.cloud.vpc:
    label: my-vpc
    region: us-east
    description: A description of this VPC.
    state: present''', '''
- name: Delete a VPC
  linode.cloud.vpc:
    label: my-vpc
    state: absent''']

result_vpc_samples = ['''{
    "created": "2023-08-31T18:35:01",
    "description": "A description of this VPC",
    "id": 344,
    "label": "my-vpc",
    "region": "us-east",
    "subnets": [],
    "updated": "2023-08-31T18:35:03"
}''']
