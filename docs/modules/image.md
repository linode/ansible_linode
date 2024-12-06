# image

Manage a Linode Image.

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
- name: Create a basic image from an existing disk
  linode.cloud.image:
    label: my-image
    description: Created using Ansible!
    disk_id: 12345
    tags: 
        - test
    state: present
```

```yaml
- name: Create a basic image from a file
  linode.cloud.image:
    label: my-image
    description: Created using Ansible!
    source_file: myimage.img.gz
    tags: 
        - test
    state: present
```

```yaml
- name: Replicate an image
  linode.cloud.image:
    label: my-image
    description: Created using Ansible!
    disk_id: 12345
    tags: 
        - test
    replica_regions: 
        - us-east
        - us-central
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
| `tags` | <center>`list`</center> | <center>Optional</center> | A list of customized tags of this new Image.  **(Updatable)** |
| `replica_regions` | <center>`list`</center> | <center>Optional</center> | A list of regions that customer wants to replicate this image in. At least one available region must be provided and only core regions allowed. Existing images in the regions not passed will be removed.   **(Updatable)** |
| `wait_for_replications` | <center>`bool`</center> | <center>Optional</center> | Wait for the all the replications `available` before returning.  **(Default: `False`)** |

## Return Values

- `image` - The Image in JSON serialized form.

    - Sample Response:
        ```json
        {
          "capabilities": [],
          "created": "2021-08-14T22:44:02",
          "created_by": "my-account",
          "deprecated": false,
          "description": "Example Image description.",
          "eol": "2026-07-01T04:00:00",
          "expiry": null,
          "id": "private/123",
          "is_public": true,
          "label": "my-image",
          "size": 2500,
          "status": null,
          "type": "manual",
          "updated": "2021-08-14T22:44:02",
          "vendor": "Debian",
          "tags": ["test"],
          "total_size": 5000,
          "regions": [
            {
                "region": "us-east",
                "status": "available"
            },
            {
                "region": "us-central",
                "status": "pending"
            }
          ]
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-image) for a list of returned fields


