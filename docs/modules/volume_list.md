# volume_list

List and filter on Linode Volumes.

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
- name: List all of the volumes that the user is allowed to view
  linode.cloud.volume_list: {}
```

```yaml
- name: Resolve all volumes that the user is allowed to view
  linode.cloud.volume_list:
    filters:
      - name: label
        values: myVolumeLabel
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list volumes in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order volumes by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting volumes.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of results to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable attributes can be found here: https://techdocs.akamai.com/linode-api/reference/get-volumes   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `volumes` - The returned volumes.

    - Sample Response:
        ```json
        [
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
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-volumes) for a list of returned fields


