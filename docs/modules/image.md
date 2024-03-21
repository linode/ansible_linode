# image

Manage a Linode Image.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create a basic image from an existing disk
  linode.cloud.image:
    label: my-image
    description: Created using Ansible!
    disk_id: 12345
    state: present
```

```yaml
- name: Create a basic image from a file
  linode.cloud.image:
    label: my-image
    description: Created using Ansible!
    source_file: myimage.img.gz
    state: present
```

```yaml
- name: Delete an image
  linode.cloud.image:
    label: my-image
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | <center>`str`</center> | <center>**Required**</center> | This Image's unique label.   |
| `state` | <center>`str`</center> | <center>**Required**</center> | The state of this Image.  **(Choices: `present`, `absent`)** |
| `cloud_init` | <center>`bool`</center> | <center>Optional</center> | Whether this image supports cloud-init.  **(Default: `False`)** |
| `description` | <center>`str`</center> | <center>Optional</center> | A description for the Image.  **(Updatable)** |
| `disk_id` | <center>`int`</center> | <center>Optional</center> | The ID of the disk to clone this image from.  **(Conflicts With: `source_file`)** |
| `recreate` | <center>`bool`</center> | <center>Optional</center> | If true, the image with the given label will be deleted and recreated  **(Default: `False`)** |
| `region` | <center>`str`</center> | <center>Optional</center> | The Linode region to upload this image to.  **(Default: `us-east`)** |
| `source_file` | <center>`str`</center> | <center>Optional</center> | An image file to create this image with.  **(Conflicts With: `disk_id`)** |
| `wait` | <center>`bool`</center> | <center>Optional</center> | Wait for the image to have status `available` before returning.  **(Default: `True`)** |
| `wait_timeout` | <center>`int`</center> | <center>Optional</center> | The amount of time, in seconds, to wait for an image to have status `available`.  **(Default: `600`)** |

## Return Values

- `image` - The Image in JSON serialized form.

    - Sample Response:
        ```json
        {
          "capabilities": [],
          "created": "2021-08-14T22:44:02",
          "created_by": "linode",
          "deprecated": false,
          "description": "Example Image description.",
          "eol": "2026-07-01T04:00:00",
          "expiry": null,
          "id": "linode/debian11",
          "is_public": true,
          "label": "Debian 11",
          "size": 2500,
          "status": null,
          "type": "manual",
          "updated": "2021-08-14T22:44:02",
          "vendor": "Debian"
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/images/#image-view__response-samples) for a list of returned fields


