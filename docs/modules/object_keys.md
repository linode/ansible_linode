# object_keys

Manage Linode Object Storage Keys.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

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

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `state` | `str` | **Required** | The desired state of the target.  (Choices:  `present`  `absent` ) |
| `label` | `str` | Optional | The unique label to give this key.   |
| [`access` (sub-options)](#access) | `list` | Optional | A list of access permissions to give the key.   |





### access

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `cluster` | `str` | **Required** | The id of the cluster that the provided bucket exists under.   |
| `bucket_name` | `str` | **Required** | The name of the bucket to set the key's permissions for.   |
| `permissions` | `str` | **Required** | The permissions to give the key.  (Choices:  `read_only`  `write_only`  `read_write` ) |






## Return Values

- `key` - The Object Storage key in JSON serialized form.

    - Sample Response:
        ```json
        {
          "access_key": "ACCESSKEY",
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
          "secret_key": "SECRETKEY"
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/object-storage/#object-storage-key-view__responses) for a list of returned fields


