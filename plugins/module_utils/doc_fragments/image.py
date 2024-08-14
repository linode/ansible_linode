"""Documentation fragments for the image module"""

specdoc_examples = ['''
- name: Create a basic image from an existing disk
  linode.cloud.image:
    label: my-image
    description: Created using Ansible!
    disk_id: 12345
    tags: 
        - test
    state: present''', '''
- name: Create a basic image from a file
  linode.cloud.image:
    label: my-image
    description: Created using Ansible!
    source_file: myimage.img.gz
    tags: 
        - test
    state: present''', '''
- name: Replicate an image
  linode.cloud.image:
    label: my-image
    description: Created using Ansible!
    disk_id: 12345
    tags: 
        - test
    replica_regions: 
        - us-east
        - us-central
    state: present''',  '''
- name: Delete an image
  linode.cloud.image:
    label: my-image
    state: absent''']

result_image_samples = ['''{
  "capabilities": [],
  "created": "2021-08-14T22:44:02",
  "created_by": "my-account",
  "deprecated": false,
  "description": "Example Image description.",
  "eol": "2026-07-01T04:00:00",
  "expiry": null,
  "id": "private/123",
  "is_public": true,
  "label": "my-image",
  "size": 2500,
  "status": null,
  "type": "manual",
  "updated": "2021-08-14T22:44:02",
  "vendor": "Debian",
  "tags": ["test"],
  "total_size": 5000,
  "regions": [
    {
        "region": "us-east",
        "status": "available"
    },
    {
        "region": "us-central",
        "status": "pending"
    }
  ]
}''']
