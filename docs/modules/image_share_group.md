# image_share_group

Manage an Image Share Group.

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
- name: Create a basic image share group
  linode.cloud.image_share_group:
    label: "my-sharegroup"
    description: "My image share group."
    state: present
```

```yaml
- name: Create a basic image share group with an image
  linode.cloud.image_share_group:
    label: "my-sharegroup"
    description: "My image share group."
    images:
      - id: "private/123"
        label: "My shared image"
        description: "An image shared in the group."
    state: present
    
```

```yaml
- name: Delete an image share group
  linode.cloud.image_share_group:
    label: "my-sharegroup"
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | <center>`str`</center> | <center>**Required**</center> | This Image Share Group's unique label.   |
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the target.  **(Choices: `present`, `absent`)** |
| `description` | <center>`str`</center> | <center>Optional</center> | A description of this Image Share Group.   |
| [`images` (sub-options)](#images) | <center>`list`</center> | <center>Optional</center> | A list of images to include in this Image Share Group.   |

### images

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>**Required**</center> | The id of the Private Image to include in an Image Share Group.   |
| `label` | <center>`str`</center> | <center>Optional</center> | A label to assign to the Image within the context of an Image Share Group.   |
| `description` | <center>`str`</center> | <center>Optional</center> | A description to assign to the Image within the context of an Image Share Group.   |

## Return Values

- `image_share_group` - The Image Share Group in JSON serialized form.

    - Sample Response:
        ```json
        {
          "created": "2025-04-14T22:44:02",
          "description": "My image share group.",
          "expiry": null,
          "id": 1,
          "images_count": 0,
          "is_suspended": false,
          "label": "my-sharegroup",
          "members_count": 0,
          "updated": null,
          "uuid": "1533863e-16a4-47b5-b829-ac0f35c13278"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-sharegroup) for a list of returned fields


