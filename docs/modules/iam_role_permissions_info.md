# iam_role_permissions_info

View IAM role permissions.

If `username` is specified, the roles assigned to that user are returned; otherwise the roles and permissions available on the account are returned.

WARNING! This module makes use of beta endpoints and requires the C(api_version) field be explicitly set to C(v4beta).

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
- name: List the roles and permissions available on the account
  linode.cloud.iam_role_permissions_info: {}
```

```yaml
- name: Get the roles assigned to a user
  linode.cloud.iam_role_permissions_info:
    username: my-user
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `username` | <center>`str`</center> | <center>Optional</center> | The username of the user to view assigned roles for. If not specified, the roles available on the account are returned.   |

## Return Values

- `role_permissions` - The returned IAM Role Permissions.

    - Sample Response:
        ```json
        {
          "account_access": [
            "account_linode_admin"
          ],
          "entity_access": [
            {
              "id": 123,
              "type": "linode",
              "roles": [
                "linode_contributor"
              ]
            }
          ]
        }
        ```
        ```json
        {
          "account_access": [
            {
              "type": "account",
              "roles": [
                {
                  "name": "account_admin",
                  "description": "Access to perform any supported action on all entities of the account",
                  "permissions": ["create_linode", "update_linode"]
                }
              ]
            }
          ],
          "entity_access": [
            {
              "type": "linode",
              "roles": [
                {
                  "name": "linode_contributor",
                  "description": "Access to update a linode instance",
                  "permissions": ["update_linode", "view_linode"]
                }
              ]
            }
          ]
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-user-role-permissions) for a list of returned fields


