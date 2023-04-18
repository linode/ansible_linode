"""Documentation fragments for the volume_list module"""

specdoc_examples = ['''
- name: List all of the volumes that the user is allowed to view
  linode.cloud.volume_list: {}''', '''
- name: Resolve all volumes that the user is allowed to view
  linode.cloud.volume_list:
    filters:
      - name: label
        values: myVolumeLabel''']

result_volumes_samples = ['''[
    {
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
    }
]''']
