# tfa_optional_users

Manage the list of account users exempt from multi-factor authentication (MFA) enforcement.

This module does not change the account-wide enforcement policy.

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
- name: Set the complete MFA exemption list
  linode.cloud.tfa_optional_users:
    usernames:
      - example-user
```

```yaml
- name: Remove all MFA exemptions
  linode.cloud.tfa_optional_users:
    usernames: []
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `usernames` | <center>`list`</center> | <center>**Required**</center> | The complete list of usernames to exempt from MFA enforcement. Users not listed lose their exemption. An empty list clears all exemptions. List order does not matter.   |

## Return Values

- `tfa_optional_users` - The current list of exempt users.

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


