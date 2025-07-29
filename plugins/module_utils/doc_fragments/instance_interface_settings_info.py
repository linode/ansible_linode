"""Documentation fragments for the vpc_info module"""

specdoc_examples = ['''
- name: Get the interface settings for an instance by label
  linode.cloud.instance_interface_settings_info:
    label: my-instance''', '''
- name: Get the interface settings for an instance by ID
  linode.cloud.instance_interface_settings_info:
    id: 12345''']
