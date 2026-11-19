# tfa_optional_user_list

List users exempt from multi-factor authentication (MFA) enforcement, regardless of the current account-wide enforcement policy.

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
- name: List users exempt from MFA enforcement
  linode.cloud.tfa_optional_user_list: {}
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `count` | <center>`int`</center> | <center>Optional</center> | The number of MFA-exempt users to return. If undefined, all results will be returned.   |

## Return Values

- `tfa_optional_users` - The returned MFA-exempt users.

    - Sample Response:
        ```json
        [
          {
            "username": "example-user",
            "url": "/account/users/example-user"
          }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-tfa-optional-users) for a list of returned fields


