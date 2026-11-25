"""Documentation fragments for the database_valkey_info module."""

specdoc_examples = ['''
- name: Get info about a Managed Valkey Database by label
  linode.cloud.database_valkey_info:
    label: my-db''', '''
- name: Get info about a Managed Valkey Database by ID
  linode.cloud.database_valkey_info:
    id: 12345''']
