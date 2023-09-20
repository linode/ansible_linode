"""Documentation fragments for the vpc_info module"""

specdoc_examples = ['''
- name: Get info about a VPC by label
  linode.cloud.vpc_info:
    label: my-vpc''', '''
- name: Get info about a VPC by ID
  linode.cloud.vpc_info:
    id: 12345''']
