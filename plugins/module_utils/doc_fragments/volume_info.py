"""Documentation fragments for the volume_info module"""

specdoc_examples = ['''
- name: Get info about a volume by label
  linode.cloud.volume_info:
    label: example-volume

- name: Get info about a volume by id
  linode.cloud.volume_info:
    id: 12345''']
