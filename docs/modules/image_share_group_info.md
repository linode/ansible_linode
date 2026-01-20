# image_share_group_info

Get info about a Linode Image Share Group.

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
- name: Get info about an Image Share Group by label
  linode.cloud.image_share_group_info:
    label: example-image-share-group
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the Image Share Group to resolve.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the Image Share Group to resolve.  **(Conflicts With: `id`)** |

## Return Values

- `image_share_group` - The returned Image Share Group.

    - Sample Response:
        ```json
        {
          "created": "2025-04-14T22:44:02",
          "description": "Example.",
          "expiry": "2025-04-14T22:44:02",
          "id": 1,
          "images_count": 0,
          "is_suspended": false,
          "label": "example-image-share-group",
          "members_count": 0,
          "updated": "2025-04-14T22:44:02",
          "uuid": "1533863e-16a4-47b5-b829-ac0f35c13278"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-sharegroup) for a list of returned fields


