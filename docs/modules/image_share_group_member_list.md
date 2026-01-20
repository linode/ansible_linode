# image_share_group_member_list

List and filter on Image Share Group Members.

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
- name: List all of the Image Share Group Members for the specified Share Group
  linode.cloud.image_share_group_member_list: 
    sharegroup_id: 123
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `sharegroup_id` | <center>`int`</center> | <center>**Required**</center> | The parent Image Share Group for the Image Share Group Members.   |
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Image Share Group Members in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Image Share Group Members by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Image Share Group Members.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Image Share Group Members to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-sharegroup-members).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `image_share_group_members` - The returned Image Share Group Members.

    - Sample Response:
        ```json
        [
            {
              "created": "2025-08-04T10:07:59",
              "expiry": "2025-08-04T10:08:01",
              "label": "member-label",
              "status": "active",
              "token_uuid": "4591075e-4ba8-43c9-a521-928c3d4a135d",
              "updated": "2025-08-04T10:08:00"
            }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-sharegroup-members) for a list of returned fields


