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

ssh_key_info_response_sample = ['''{
  "created": "2018-01-01T00:01:01",
  "id": 42,
  "label": "My SSH Key",
  "ssh_key": "ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer"
}''']
