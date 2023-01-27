"""Documentation fragments for the ssh_key_list module"""

ssh_key_list_specdoc_examples = ['''
- name: List all of the SSH keys for the current Linode Account
  linode.cloud.ssh_key_list: {}''', '''
- name: List the latest 5 SSH keys for the current Linode Account
  linode.cloud.ssh_key_list:

    count: 5
    order_by: created
    order: desc''', '''
- name: List filtered personal SSH keys for the current Linode Account
  linode.cloud.ssh_key_list:

    filters:
      - name: label-or-some-other-field
        values: MySSHKey1''', '''
- name: List filtered personal SSH keys for the current Linode Account
  linode.cloud.ssh_key_list:
    filters:
      - name: label-or-some-other-field
        values:
          - MySSHKey1
          - MySSHKey2''']

result_ssh_key_list_samples = ['''[
    {
      "created": "2018-01-01T00:01:01",
      "id": 42,
      "label": "MySSHKey1",
      "ssh_key": "ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer"
    }
]''']
