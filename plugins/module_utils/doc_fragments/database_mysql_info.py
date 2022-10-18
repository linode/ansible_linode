"""Documentation fragments for the database_mysql_info module"""

specdoc_examples = ['''
- name: Get info about a Managed MySQL Database by label
  linode.cloud.database_mysql_info:
    label: my-db''', '''
- name: Get info about a Managed MySQL Database by ID
  linode.cloud.database_mysql_info:
    id: 12345''']
