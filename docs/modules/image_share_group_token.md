# image_share_group_token

Manage an Image Share Group Token.

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
- name: Create an image share group token
  linode.cloud.image_share_group_token:
    label: "my-sharegroup-token"
    valid_for_sharegroup_uuid: "1533863e-16a4-47b5-b829-ac0f35c13278"
    state: present
```

```yaml
- name: Delete an image share group token
  linode.cloud.image_share_group_token:
    label: "my-sharegroup-token"
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | <center>`str`</center> | <center>**Required**</center> | This Image Share Group Token's unique label.   |
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the target.  **(Choices: `present`, `absent`)** |
| `valid_for_sharegroup_uuid` | <center>`str`</center> | <center>Optional</center> | The UUID of the Image Share Group that this token is valid for.   |

## Return Values

- `image_share_group_token` - The Image Share Group Token in JSON serialized form.

    - Sample Response:
        ```json
        {
          "created": "2025-08-04T10:09:09",
          "expiry": null,
          "label": "Backend Services - Engineering",
          "sharegroup_label": "DevOps Base Images",
          "sharegroup_uuid": "e1d0e58b-f89f-4237-84ab-b82077342359",
          "status": "active",
          "token_uuid": "13428362-5458-4dad-b14b-8d0d4d648f8c",
          "updated": null,
          "valid_for_sharegroup_uuid": "e1d0e58b-f89f-4237-84ab-b82077342359"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-sharegroup-token) for a list of returned fields


- `single_use_token` - The single use token string to provide to a Image Share Group Producer to be added to the share group.

    - Sample Response:
        ```json
        {
          "token": "abcdefghijklmnopqrstuvwxyz1234567890"
        }
        ```


