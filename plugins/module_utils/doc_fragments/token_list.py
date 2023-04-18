"""Documentation fragments for the token_list module"""

specdoc_examples = ['''
- name: List all of the Personal Access Tokens active for the current user
  linode.cloud.token_list: {}''', '''
- name: Resolve all of the Personal Access Tokens active for the current user
  linode.cloud.token_list:
    filters:
      - name: label
        values: myTokenLabel''']

result_tokens_samples = ['''[
    {
      "created": "2018-01-01T00:01:01",
      "expiry": "2018-01-01T13:46:32",
      "id": 123,
      "label": "linode-cli",
      "scopes": "*",
      "token": "abcdefghijklmnop"
    }
]''']
