"""Documentation fragments for the nodebalancer_info module"""

specdoc_examples = ['''
- name: Get a NodeBalancer by its id
  linode.cloud.nodebalancer_info:
    id: 12345''', '''
- name: Get a NodeBalancer by its label
  linode.cloud.nodebalancer_info:
    label: cool_nodebalancer''']
