"""Documentation fragments for the volume module"""

specdoc_examples = ['''
- name: Create a volume attached to an instance
  linode.cloud.volume:
    label: example-volume
    region: us-east
    size: 30
    linode_id: 12345
    state: present''', '''
- name: Create an unattached volume
  linode.cloud.volume:
    label: example-volume
    region: us-east
    size: 30
    state: present''', '''
- name: Resize a volume
  linode.cloud.volume:
    label: example-volume
    size: 50
    state: present''', '''
- name: Detach a volume
  linode.cloud.volume:
    label: example-volume
    attached: false
    state: present''', '''
- name: Delete a volume
  linode.cloud.volume:
    label: example-volume
    state: absent
- name: Create an cloned volume
  linode.cloud.volume: 
    source_volume_id: 1234
    label: example-volume
    region: us-east
    size: 30
    state: present''']

result_volume_samples = ['''{
  "created": "2018-01-01T00:01:01",
  "filesystem_path": "/dev/disk/by-id/scsi-0Linode_Volume_my-volume",
  "hardware_type": "nvme",
  "id": 12345,
  "label": "my-volume",
  "linode_id": 12346,
  "linode_label": "linode123",
  "region": "us-east",
  "size": 30,
  "status": "active",
  "tags": [
    "example tag",
    "another example"
  ],
  "updated": "2018-01-01T00:01:01"
}''']
