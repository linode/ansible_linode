# volume_list

List and filter on Linode Volumes.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

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
| `api_token` | <center>`str`</center> | <center>Optional</center> | The Linode account personal access token. It is necessary to run the module. It can be exposed by the environment variable `LINODE_API_TOKEN` instead.   |
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list volumes in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order volumes by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting volumes.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of results to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable attributes can be found here: https://www.linode.com/docs/api/volumes/#volumes-list__responses   |
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
    - See the [Linode API response documentation](https://www.linode.com/docs/api/volumes/#volumes-list__response-samples) for a list of returned fields


