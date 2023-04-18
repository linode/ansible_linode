"""Documentation fragments for the database_engine_list module"""

specdoc_examples = ['''
- name: List all of the available Managed Database engine types
  linode.cloud.database_engine_list: {}''', '''
- name: Resolve all Database engine types
  linode.cloud.database_engine_list:
    filters:
      - name: engine
        values: mysql''']

result_engines_samples = ['''[
   {
      "engine": "mysql",
      "id": "mysql/8.0.30",
      "version": "8.0.30"
    }
]''']
