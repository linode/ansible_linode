"""Documentation fragments for the firewall_info module"""

specdoc_examples = ['''
- name: Get info about a Firewall by label
  linode.cloud.firewall_info:
    label: 'my-firewall' ''', '''
- name: Get info about a Firewall by id
  linode.cloud.firewall_info:
    id: 12345''']
