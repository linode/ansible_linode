"""Documentation fragments for the vpc_info module"""

specdoc_examples = ['''
- name: Get info about a VPC Subnet by label
  linode.cloud.vpc_subnet_info:
    vpc_id: 12345
    label: my-subnet''', '''
- name: Get info about a VPC Subnet by ID
  linode.cloud.vpc_subnet_info:
    vpc_id: 12345
    id: 123''']
