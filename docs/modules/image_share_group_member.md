# image_share_group_member

Manage an Image Share Group Member.

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
- name: Create an image share group member
  linode.cloud.image_share_group_member:
    label: "my-sharegroup-member"
    token: "abcdefghijklmnopqrstuvwxyz1234567890"
    state: present
```

```yaml
- name: Delete an image share group member
  linode.cloud.image_share_group_member:
    label: "my-sharegroup-member"
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | <center>`str`</center> | <center>**Required**</center> | This Image Share Group Member's unique label.   |
| `sharegroup_id` | <center>`int`</center> | <center>**Required**</center> | The ID of the Image Share Group this member belongs to.   |
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the target.  **(Choices: `present`, `absent`)** |
| `token` | <center>`str`</center> | <center>Optional</center> | A single-use Image Share Group Token provided by the Consumer. This value is required when creating a member and is never returned.   |

## Return Values

- `image_share_group_member` - The Image Share Group Member in JSON serialized form.

    - Sample Response:
        ```json
        {
           "token_uuid": "24wef-243qg-45wgg-q343q",
           "status": "active",
           "label": "my-sharegroup-member",
           "created": "2016-03-16T17:30:49", 
           "updated": "2016-03-18T17:30:49", 
           "expiry": "2016-03-18T17:30:49"
        }
        
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-sharegroup-member-token) for a list of returned fields


