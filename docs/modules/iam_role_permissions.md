# iam_role_permissions

Update the roles assigned to a user.

The specified roles replace the user's existing roles.

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
- name: Assign roles to a user
  linode.cloud.iam_role_permissions:
    username: my-user
    account_access:
      - account_linode_admin
    entity_access:
      - id: 123
        type: linode
        roles:
          - linode_contributor
```

```yaml
- name: Remove all entity-level roles from a user
  linode.cloud.iam_role_permissions:
    username: my-user
    entity_access: []
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `username` | <center>`str`</center> | <center>**Required**</center> | The username of the user to assign roles to.   |
| `account_access` | <center>`list`</center> | <center>Optional</center> | The account-level roles to assign to the user. If omitted, the user's current account-level roles are preserved.  **(Updatable)** |
| [`entity_access` (sub-options)](#entity_access) | <center>`list`</center> | <center>Optional</center> | The entity-level roles to assign to the user. If omitted, the user's current entity-level roles are preserved. Specify an empty list to remove all entity-level roles.  **(Updatable)** |
| `state` | <center>`str`</center> | <center>Optional</center> | The desired state of the target.  **(Choices: `present`)** |

### entity_access

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>**Required**</center> | The ID of the entity.   |
| `type` | <center>`str`</center> | <center>**Required**</center> | The type of the entity (e.g. `linode`, `firewall`).   |
| `roles` | <center>`list`</center> | <center>**Required**</center> | The roles the user has on the entity.   |

## Return Values

- `role_permissions` - The user's role permissions.

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
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/put-user-role-permissions) for a list of returned fields


