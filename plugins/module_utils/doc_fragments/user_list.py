"""Documentation fragments for the user_list module"""

specdoc_examples = ['''
- name: List all of the users for the current Linode Account
  linode.cloud.user_list: {}''',
'''
- name: List users required to use MFA
  linode.cloud.user_list:
    filters:
      - name: tfa_enforced
        values: ["true"]''']

result_users_samples = ['''[
  {
    "email": "example_user@linode.com",
    "restricted": true,
    "user_type": "default",
    "ssh_keys": [
      "home-pc",
      "laptop"
    ],
    "tfa_enabled": null,
    "tfa_enforced": true,
    "username": "example_user"
  }
]''']
