"""Documentation fragments for the ssh_key_info module"""

specdoc_examples = [
'''
- name: Get info about a SSH key by label
  linode.cloud.ssh_key_info:
    label: my-ssh-key''',
'''
- name: Get info about a SSH key by ID
  linode.cloud.ssh_key_info:
    id: 12345''']
