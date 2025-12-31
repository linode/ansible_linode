# image_share_group_token_info

Get info about a Linode Image Share Group Token.

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
- name: Get info about an Image Share Group Token by label
  linode.cloud.image_share_group_token_info:
    label: example-image-share-group-token
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `token_uuid` | <center>`str`</center> | <center>Optional</center> | The Token UUID of the Image Share Group Token to resolve.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the Image Share Group Token to resolve.  **(Conflicts With: `token_uuid`)** |

## Return Values

- `image_share_group_token` - The returned Image Share Group Token.

    - Sample Response:
        ```json
        {
            "created": "2025-08-04T10:09:09",
            "expiry": "2025-08-04T10:09:11",
            "label": "example-token",
            "sharegroup_label": "example-sharegroup",
            "sharegroup_uuid": "e1d0e58b-f89f-4237-84ab-b82077342359",
            "status": "active",
            "token_uuid": "13428362-5458-4dad-b14b-8d0d4d648f8c",
            "updated": "2025-08-04T10:09:10",
            "valid_for_sharegroup_uuid": "e1d0e58b-f89f-4237-84ab-b82077342359"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-sharegroup-token) for a list of returned fields


