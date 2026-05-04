# monitor_logs_destination_list

List and filter on Logs Destinations.

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
- name: List all of available logs destinations to the account
  linode.cloud.monitor_logs_destination_list: {}
```

```yaml
- name: List all of available logs destinations to the account with label filter
  linode.cloud.monitor_logs_destination_list:
    filters:
      - name: label
        values: my_logs_destination_label
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Logs Destinations in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Logs Destinations by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Logs Destinations.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Logs Destinations to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-destinations).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `logs_destinations` - The returned Logs Destinations.

    - Sample Response:
        ```json
        [
            {
              "created": "2025-07-20 09:45:13",
              "created_by": "John Q. Linode",
              "details": {
                "access_key_id": 123,
                "bucket_name": "primary-bucket",
                "host": "primary-bucket-1.us-iad-12.linodeobjects.com",
                "path": "audit-logs-logs"
              },
              "id": 12345,
              "label": "OBJ_logs_destination",
              "status": "active",
              "type": "akamai_object_storage",
              "updated": "2025-07-21 12:41:09",
              "updated_by": "Jane Q. Linode",
              "version": 2
            },
            {
              "created": "2025-07-21 10:30:15",
              "created_by": "Jane Q. Linode",
              "details": {
                "access_key_id": 456,
                "bucket_name": "secondary-bucket",
                "host": "secondary-bucket-1.us-iad-12.linodeobjects.com",
                "path": "audit-logs-backup"
              },
              "id": 12345,
              "label": "OBJ_logs_backup_destination",
              "status": "inactive",
              "type": "akamai_object_storage",
              "updated": "2025-07-21 10:30:15",
              "updated_by": "Jane Q. Linode",
              "version": 1
            }
          ]
        
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-destinations) for a list of returned fields


