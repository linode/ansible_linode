"""Documentation fragments for the user_list module"""

specdoc_examples = ['''
- name: List all of the users for the current Linode Account
  linode.cloud.user_list: {}''']

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
    "username": "example_user"
  }
]''']
