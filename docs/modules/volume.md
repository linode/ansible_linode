# volume

Manage a Linode Volume.

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
- name: Create a volume attached to an instance
  linode.cloud.volume:
    label: example-volume
    region: us-east
    size: 30
    linode_id: 12345
    state: present
```

```yaml
- name: Create an unattached volume
  linode.cloud.volume:
    label: example-volume
    region: us-east
    size: 30
    state: present
```

```yaml
- name: Resize a volume
  linode.cloud.volume:
    label: example-volume
    size: 50
    state: present
```

```yaml
- name: Detach a volume
  linode.cloud.volume:
    label: example-volume
    attached: false
    state: present
```

```yaml
- name: Delete a volume
  linode.cloud.volume:
    label: example-volume
    state: absent
- name: Create an cloned volume
  linode.cloud.volume: 
    source_volume_id: 1234
    label: example-volume
    region: us-east
    size: 30
    state: present
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the target.  **(Choices: `present`, `absent`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The Volume’s label, which is also used in the filesystem_path of the resulting volume.   |
| `config_id` | <center>`int`</center> | <center>Optional</center> | When creating a Volume attached to a Linode, the ID of the Linode Config to include the new Volume in.   |
| `linode_id` | <center>`int`</center> | <center>Optional</center> | The Linode this volume should be attached to upon creation. If not given, the volume will be created without an attachment.  **(Updatable)** |
| `region` | <center>`str`</center> | <center>Optional</center> | The location to deploy the volume in. See https://api.linode.com/v4/regions   |
| `size` | <center>`int`</center> | <center>Optional</center> | The size of this volume, in GB. Be aware that volumes may only be resized up after creation.  **(Updatable)** |
| `attached` | <center>`bool`</center> | <center>Optional</center> | If true, the volume will be attached to a Linode. Otherwise, the volume will be detached.  **(Default: `True`; Updatable)** |
| `encryption` | <center>`str`</center> | <center>Optional</center> | Enables encryption on the volume. Full disk encryption ensures the data stored on a block storage volume drive is secure.  **(Choices: `disabled`, `enabled`)** |
| `wait_timeout` | <center>`int`</center> | <center>Optional</center> | The amount of time, in seconds, to wait for a volume to have the active status.  **(Default: `240`)** |
| `source_volume_id` | <center>`int`</center> | <center>Optional</center> | The volume id of the desired volume to clone.   |
| `tags` | <center>`list`</center> | <center>Optional</center> | The tags to be attached to the volume.   |

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
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-volume) for a list of returned fields


