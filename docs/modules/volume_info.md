# volume_info

Get info about a Linode Volume.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Get info about a volume by label
  linode.cloud.volume_info:
    label: example-volume

- name: Get info about a volume by id
  linode.cloud.volume_info:
    id: 12345
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the Volume. Optional if `label` is defined.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the Volume. Optional if `id` is defined.  **(Conflicts With: `id`)** |

## Return Values

- `volume` - The volume in JSON serialized form.

    - Sample Response:
        ```json
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
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/volumes/#volume-view__responses) for a list of returned fields


