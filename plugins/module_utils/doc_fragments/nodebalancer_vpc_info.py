"""Documentation fragments for the nodebalancer_vpc_info module"""

specdoc_examples = ['''
- name: Get a NodeBalancer VPC configuration by its id
  linode.cloud.nodebalancer_vpc_info:
    id: 12345
    vpc_config_id: 123''', '''
- name: Get a NodeBalancer by its label
  linode.cloud.nodebalancer_vpc_info:
    label: cool_nodebalancer
    vpc_config_id: 123''']
