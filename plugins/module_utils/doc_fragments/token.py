"""Documentation fragments for the token module"""

specdoc_examples = ['''
- name: Create a simple token 
  linode.cloud.token:
    label: my-token
    state: present''', '''
- name: Create a token with expiry date and scopes 
  linode.cloud.token:
    label: my-token
    expiry: 2022-07-09T16:59:26
    scope: '*'
    state: present''', '''
- name: Delete a token
  linode.cloud.token:
    label: my-token
    state: absent''']

result_token_samples = ['''{
  "created": "2018-01-01T00:01:01",
  "expiry": "2018-01-01T13:46:32",
  "id": 123,
  "label": "linode-cli",
  "scopes": "*",
  "token": "abcdefghijklmnop"
}''']
