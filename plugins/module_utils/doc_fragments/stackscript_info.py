"""Documentation fragments for the stackscript_info module"""

specdoc_examples = ['''
- name: Get info about a StackScript by label
  linode.cloud.stackscript_info:
    label: my-stackscript''', '''
- name: Get info about a StackScript by ID
  linode.cloud.stackscript_info:
    id: 12345''']
