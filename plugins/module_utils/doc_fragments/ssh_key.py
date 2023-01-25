"""Documentation fragments for the volume module"""

specdoc_examples = ['''
- name: Create a basic SSH key
  linode.cloud.ssh_key:
    api_token: "{{ api_token }}"
    ua_prefix: "{{ ua_prefix }}"
    label: my-ssh-key
    state: present''', '''
- name: Delete a SSH key
  linode.cloud.ssh_key:
    api_token: "{{ api_token }}"
    ua_prefix: "{{ ua_prefix }}"
    label: my-ssh-key
    state: absent''']

result_ssh_key_samples = ['''{
  "created": "2018-01-01T00:01:01",
  "id": 42,
  "label": "My SSH Key",
  "ssh_key": "ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer"
}''',
"{}"]
