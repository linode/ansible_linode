"""Documentation fragments for the database_mongodb_info module"""

specdoc_examples = ['''
- name: Get info about a Managed Mongo Database by label
  linode.cloud.database_mongodb_info:
    label: my-db''', '''
- name: Get info about a Managed Mongo Database by ID
  linode.cloud.database_mongodb_info:
    id: 12345''']
