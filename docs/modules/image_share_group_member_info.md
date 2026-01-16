# image_share_group_member_info

Get info about a Linode Image Share Group Member.

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
- name: Get info about an Image Share Group Member by label
  linode.cloud.image_share_group_member_info:
    sharegroup_id: 123456
    label: example-image-share-group-member
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `sharegroup_id` | <center>`int`</center> | <center>**Required**</center> | The ID of the Image Share Group for this resource.   |
| `token_uuid` | <center>`str`</center> | <center>Optional</center> | The Token UUID of the Image Share Group Member to resolve.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the Image Share Group Member to resolve.  **(Conflicts With: `token_uuid`)** |

## Return Values

- `image_share_group_member` - The returned Image Share Group Member.

    - Sample Response:
        ```json
        {
          "created": "2025-08-04T10:07:59",
          "expiry": "2025-08-04T10:08:01",
          "label": "Engineering - Backend",
          "status": "active",
          "token_uuid": "4591075e-4ba8-43c9-a521-928c3d4a135d",
          "updated": "2025-08-04T10:08:00"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-sharegroup-member-token) for a list of returned fields


