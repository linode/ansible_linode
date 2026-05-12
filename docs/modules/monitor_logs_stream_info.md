# monitor_logs_stream_info

Get info about a Linode Monitor Logs Stream.

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
- name: Get info about a logs stream by ID
  linode.cloud.monitor_logs_stream_info:
    id: 12345

- name: Get info about a logs stream by label
  linode.cloud.monitor_logs_stream_info:
    label: "my-audit-logs"

```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the Monitor Logs Stream to resolve.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the Monitor Logs Stream to resolve.  **(Conflicts With: `id`)** |

## Return Values

- `stream` - The returned Monitor Logs Stream.

    - Sample Response:
        ```json
        {
                "created": "2025-03-20 01:41:09",
                "created_by": "John Q. Linode",
                "destinations": [
                    {
                        "details": {
                            "access_key_id": "123",
                            "bucket_name": "primary-bucket",
                            "host": "primary-bucket-1.us-iad-12.linodeobjects.com",
                            "path": "audit-logs"
                        },
                        "id": 12345,
                        "label": "OBJ_logs_destination",
                        "type": "akamai_object_storage"
                    }
                ],
                "id": 12345,
                "label": "AuditLog-config",
                "status": "active",
                "type": "audit_logs",
                "updated": "2025-03-20 01:41:09",
                "updated_by": "Jane Q. Linode",
                "version": 1
            }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-stream) for a list of returned fields


