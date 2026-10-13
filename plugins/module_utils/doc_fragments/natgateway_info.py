"""Documentation fragments for the natgateway_info module"""

specdoc_examples = ['''
- name: Get info about a NAT Gateway by label
  linode.cloud.natgateway_info:
    label: my-nat-gateway''', '''
- name: Get info about a NAT Gateway by ID
  linode.cloud.natgateway_info:
    id: 123''']
