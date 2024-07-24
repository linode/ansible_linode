# object_keys

Manage Linode Object Storage Keys.

- [Minimum Required Fields](#minimum-required-fields)
- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Minimum Required Fields
| Field       | Type  | Required     | Description                                                                                                                                                                                                              |
|-------------|-------|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `api_token` | `str` | **Required** | The Linode account personal access token. It is necessary to run the module. <br/>It can be exposed by the environment variable `LINODE_API_TOKEN` instead. <br/>See details in [Usage](https://github.com/linode/ansible_linode?tab=readme-ov-file#usage). |

## Examples

```yaml
- name: Create an Object Storage key
  linode.cloud.object_keys:
    label: 'my-fullaccess-key'
    state: present
```

```yaml
- name: Create an Object Storage key limited to specific regions
  linode.cloud.object_keys:
    label: 'my-region-limited-key'
    regions:
        - us-mia
        - us-ord
    state: present
```

```yaml
- name: Create an Object Storage key limited to specific buckets
  linode.cloud.object_keys:
    label: 'my-limited-key'
    access:
      - cluster: us-mia
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
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the target.  **(Choices: `present`, `absent`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The unique label to give this key.   |
| [`access` (sub-options)](#access) | <center>`list`</center> | <center>Optional</center> | A list of access permissions to give the key.   |
| `regions` | <center>`list`</center> | <center>Optional</center> | A list of regions to scope this key to.  **(Updatable)** |

### access

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `bucket_name` | <center>`str`</center> | <center>**Required**</center> | The name of the bucket to set the key's permissions for.   |
| `permissions` | <center>`str`</center> | <center>**Required**</center> | The permissions to give the key.  **(Choices: `read_only`, `write_only`, `read_write`)** |
| `region` | <center>`str`</center> | <center>Optional</center> | The region of the cluster that the provided bucket exists under.  **(Conflicts With: `cluster`)** |
| `cluster` | <center>`str`</center> | <center>Optional</center> | The id of the cluster that the provided bucket exists under. **NOTE: This field has been deprecated because it relies on deprecated API endpoints. Going forward, `region` will be the preferred way to designate where Object Storage resources should be created.**  **(Conflicts With: `region`)** |

## Return Values

- `key` - The Object Storage key in JSON serialized form.

    - Sample Response:
        ```json
        {
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
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-object-storage-key) for a list of returned fields


