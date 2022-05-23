# object_keys

Manage Linode Object Storage Keys.


## Examples

```yaml
- name: Create an Object Storage key
  linode.cloud.object_keys:
    label: 'my-fullaccess-key'
    state: present
```

```yaml
- name: Create a limited Object Storage key
  linode.cloud.object_keys:
    label: 'my-limited-key'
    access:
      - cluster: us-east-1
        bucket_name: my-bucket
        permissions: read_write
    state: present
```

```yaml
- name: Remove an object storage key
  linode.cloud.object_keys:
    label: 'my-key'
    state: absent
```


## Parameters


- `label` -  The unique label to give this key. 
- `access` -  A list of access permissions to give the key. 
    - `cluster` - **(Required)** The id of the cluster that the provided bucket exists under. 
    - `bucket_name` - **(Required)** The name of the bucket to set the key's permissions for. 
    - `permissions` - **(Required)** The permissions to give the key. 


## Return Values

- `key` - The Object Storage key in JSON serialized form.

    - Sample Response:
        ```json
        {
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
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/object-storage/#object-storage-key-view__responses) for a list of returned fields


