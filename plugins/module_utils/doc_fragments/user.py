"""Documentation fragments for the user module"""

specdoc_examples = ['''
- name: Create a basic user
  linode.cloud.user:
    username: my-cool-user
    email: user@linode.com
    restricted: false
    state: present''', '''
- name: Delete a user
  linode.cloud.user:
    username: my-cool-user
    state: absent''']

result_user_samples = ['''{
  "email": "example_user@linode.com",
  "restricted": true,
  "ssh_keys": [
    "home-pc",
    "laptop"
  ],
  "tfa_enabled": null,
  "username": "example_user"
}''']
