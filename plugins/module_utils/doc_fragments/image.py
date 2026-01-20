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
  "capabilities": [
    "cloud-init",
    "distributed-sites"
  ],
  "created": "2021-08-14T22:44:02",
  "created_by": "linode",
  "deprecated": false,
  "description": "Example image description.",
  "eol": "2026-07-01T04:00:00",
  "expiry": null,
  "id": "private/15",
  "image_sharing": {
    "shared_by": null,
    "shared_with": {
      "sharegroup_count": 0,
      "sharegroup_list_url": "/images/private/15/sharegroups"
    }
  },
  "is_public": false,
  "is_shared": false,
  "label": "Debian 11",
  "regions": [
    {
      "region": "us-iad",
      "status": "available"
    }
  ],
  "size": 2500,
  "status": "available",
  "tags": [
    "repair-image",
    "fix-1"
  ],
  "total_size": 1234567,
  "type": "manual",
  "updated": "2021-08-14T22:44:02",
  "vendor": "Debian"
}''']
