"""Documentation fragments for the token_info module"""

specdoc_examples = ['''
- name: Get info about a token by label
  linode.cloud.token_info:
    label: my-token''', '''
- name: Get info about a token by ID
  linode.cloud.token_info:
    id: 12345''']
