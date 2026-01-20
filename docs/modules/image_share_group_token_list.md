# image_share_group_token_list

List and filter on Image Share Group Tokens.

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
- name: List all of the Image Share Group Tokens for the current Linode Account
  linode.cloud.image_share_group_token_list: {}
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Image Share Group Tokens in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Image Share Group Tokens by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Image Share Group Tokens.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Image Share Group Tokens to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-user-tokens).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `image_share_group_tokens` - The returned Image Share Group Tokens.

    - Sample Response:
        ```json
        [
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
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-user-tokens) for a list of returned fields


