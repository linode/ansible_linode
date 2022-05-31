"""Documentation fragments for the instance_info module"""

specdoc_examples = ['''
- name: Get info about an instance by label
  linode.cloud.instance_info:
    label: 'my-instance' ''', '''
- name: Get info about an instance by id
  linode.cloud.instance_info:
    id: 12345''']
