"""Documentation fragments for the image module"""

specdoc_examples = ['''
- name: Create a basic image from an existing disk
  linode.cloud.image:
    label: my-image
    description: Created using Ansible!
    disk_id: 12345
    state: present''', '''
- name: Create a basic image from a file
  linode.cloud.image:
    label: my-image
    description: Created using Ansible!
    source_file: myimage.img.gz
    state: present''', '''
- name: Delete an image
  linode.cloud.image:
    label: my-image
    state: absent''']

result_image_samples = ['''{
  "capabilities": [],
  "created": "2021-08-14T22:44:02",
  "created_by": "linode",
  "deprecated": false,
  "description": "Example Image description.",
  "eol": "2026-07-01T04:00:00",
  "expiry": null,
  "id": "linode/debian11",
  "is_public": true,
  "label": "Debian 11",
  "size": 2500,
  "status": null,
  "type": "manual",
  "updated": "2021-08-14T22:44:02",
  "vendor": "Debian"
}''']
