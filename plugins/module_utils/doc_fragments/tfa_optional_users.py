"""Documentation fragments for the tfa_optional_users module."""

specdoc_examples = [
    '''
- name: Set the complete MFA exemption list
  linode.cloud.tfa_optional_users:
    usernames:
      - example-user''',
    '''
- name: Remove all MFA exemptions
  linode.cloud.tfa_optional_users:
    usernames: []''',
]

result_tfa_optional_users_samples = ['''[
  {
    "username": "example-user",
    "url": "/account/users/example-user"
  }
]''']
