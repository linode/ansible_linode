"""Documentation fragments for the image_info module"""

specdoc_examples = ['''
- name: Get info about an image by label
  linode.cloud.image_info:
    label: my-image''', '''
- name: Get info about an image by ID
  linode.cloud.image_info:
    id: private/12345''']
