"""Documentation fragments for the object_keys module"""

specdoc_examples = ['''
- name: Create an Object Storage key
  linode.cloud.object_keys:
    label: 'my-fullaccess-key'
    state: present''', '''
- name: Create an Object Storage key limited to specific regions
  linode.cloud.object_keys:
    label: 'my-region-limited-key'
    regions:
        - us-mia
        - us-ord
    state: present''', '''
- name: Create an Object Storage key limited to specific buckets
  linode.cloud.object_keys:
    label: 'my-limited-key'
    access:
      - cluster: us-mia
        bucket_name: my-bucket
        permissions: read_write
    state: present''', '''
- name: Remove an object storage key
  linode.cloud.object_keys:
    label: 'my-key'
    state: absent''']

result_key_samples = ['''{
  "access_key": "redacted",
  "bucket_access": [
    {
      "bucket_name": "my-bucket",
      "cluster": "us-iad-1",
      "permissions": "read_write",
      "region": "us-iad"
    }
  ],
  "id": 12345,
  "label": "my-key",
  "limited": true,
  "regions": [
    {
      "id": "us-iad",
      "s3_endpoint": "us-iad-1.linodeobjects.com"
    },
    {
      "id": "us-ord",
      "s3_endpoint": "us-ord-1.linodeobjects.com"
    },
    {
      "id": "us-sea",
      "s3_endpoint": "us-sea-1.linodeobjects.com"
    }
  ],
  "secret_key": "[REDACTED]"
}''']
