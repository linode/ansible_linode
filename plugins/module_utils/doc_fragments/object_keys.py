"""Documentation fragments for the object_keys module"""

specdoc_examples = ['''
- name: Create an Object Storage key
  linode.cloud.object_keys:
    label: 'my-fullaccess-key'
    state: present''', '''
- name: Create a limited Object Storage key
  linode.cloud.object_keys:
    label: 'my-limited-key'
    access:
      - cluster: us-east-1
        bucket_name: my-bucket
        permissions: read_write
    state: present''', '''
- name: Remove an object storage key
  linode.cloud.object_keys:
    label: 'my-key'
    state: absent''']

result_key_samples = ['''{
  "access_key": "KVAKUTGBA4WTR2NSJQ81",
  "bucket_access": [
    {
      "bucket_name": "example-bucket",
      "cluster": "ap-south-1",
      "permissions": "read_only"
    }
  ],
  "id": 123,
  "label": "my-key",
  "limited": true,
  "secret_key": "OiA6F5r0niLs3QA2stbyq7mY5VCV7KqOzcmitmHw"
}''']
