# monitor_logs_stream_list

List and filter on Monitor Logs Streams.

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
- name: List all logs streams
  linode.cloud.monitor_logs_stream_list:
  register: all_streams

- name: List logs streams with active status
  linode.cloud.monitor_logs_stream_list:
    filters:
      - name: status
        values:
          - active
  register: active_streams

```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Monitor Logs Streams in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Monitor Logs Streams by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Monitor Logs Streams.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Monitor Logs Streams to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-streams).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `streams` - The returned Monitor Logs Streams.

    - Sample Response:
        ```json
        [
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
            ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-streams) for a list of returned fields


