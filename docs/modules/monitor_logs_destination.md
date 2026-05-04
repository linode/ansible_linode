# monitor_logs_destination

Manage logs destination that sevres as a sync point for logs data. It can only be accessed by account users with unrestricted access. 

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
- name: Create a logs destination
  linode.cloud.monitor_logs_destination:
    label: 'test-logs-destination'
    type: 'akamai_object_storage'
    details:
      access_key_id: '{{ access_key_id }}'
      access_key_secret: '{{ access_key_secret }}'
      bucket_name: '{{ bucket_name }}'
      host: '{{ host }}'
      path: 'test-path'
    state: present
```

```yaml
- name: Delete logs destination
  linode.cloud.monitor_logs_destination:
    id: 12345
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the target.  **(Choices: `present`, `absent`)** |
| [`details` (sub-options)](#details) | <center>`dict`</center> | <center>Optional</center> | Settings used for an Object Storage-based destination for a stream. You need an existing Object Storage bucket, configured to use Object Lock.  **(Updatable)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The name of the destination object. Used for display purposes.  **(Updatable)** |
| `type` | <center>`str`</center> | <center>Optional</center> | The type of destination for logs data sync.Currently, only akamai_object_storage is supported for use. This lets you use Akamai Object Storage as your destination.  **(Choices: `akamai_object_storage`; Updatable)** |
| `id` | <center>`int`</center> | <center>Optional</center> | The unique identifier assigned to the logs destination. Run the List logs destinations operation and store the id for the applicable logs destination. Required for updating.   |
| `wait` | <center>`bool`</center> | <center>Optional</center> | Wait for the logs destination ready.  **(Default: `False`)** |
| `wait_timeout` | <center>`int`</center> | <center>Optional</center> | The amount of time, in seconds, to wait for the logs destination.  **(Default: `600`)** |

### details

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `access_key_id` | <center>`str`</center> | <center>Optional</center> | The unique identifier assigned to the Object Storage key required for authentication to the bucket. Run the List Object Storage keys operation and store the id for the applicable key.  **(Updatable)** |
| `access_key_secret` | <center>`str`</center> | <center>Optional</center> | The Object Storage key's secret key. This is used as a password to validate the key.  **(Updatable)** |
| `bucket_name` | <center>`str`</center> | <center>Optional</center> | The name of the Object Storage bucket. Run the List Object Storage buckets operation and store the label for the target bucket.  **(Updatable)** |
| `host` | <center>`str`</center> | <center>Optional</center> | The hostname where the Object Storage bucket can be accessed. Run the List Object Storage buckets operation and store the hostname for the target bucket.  **(Updatable)** |
| `path` | <center>`str`</center> | <center>Optional</center> | Include this object to set a custom path for audit log storage in your Object Storage bucket.  **(Updatable)** |

## Return Values

- `logs_destination` - The logs destination in JSON serialized form.

    - Sample Response:
        ```json
        {
          "created": "2025-07-20 09:45:13",
          "created_by": "John Q. Linode",
          "details": {
            "access_key_id": 123,
            "bucket_name": "primary-bucket",
            "host": "primary-bucket-1.us-iad-12.linodeobjects.com",
            "path": "audit-logs"
          },
          "id": 12345,
          "label": "OBJ_logs_destination",
          "status": "active",
          "type": "akamai_object_storage",
          "updated": "2025-07-21 12:41:09",
          "updated_by": "Jane Q. Linode",
          "version": 1
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-destination) for a list of returned fields


