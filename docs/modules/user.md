# user

Manage a Linode User.

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
- name: Create a basic user
  linode.cloud.user:
    username: my-cool-user
    email: user@linode.com
    restricted: false
    state: present
```

```yaml
- name: Create a user that can only access Linodes
  linode.cloud.user:
    username: my-cool-user
    email: user@linode.com
    grants:
      global:
        add_linodes: true
      resources:
        - type: linode
          id: 12345
          permissions: read_write
    state: present
```

```yaml
- name: Delete a user
  linode.cloud.user:
    username: my-cool-user
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `username` | <center>`str`</center> | <center>**Required**</center> | The username of this user.   |
| `state` | <center>`str`</center> | <center>**Required**</center> | The state of this user.  **(Choices: `present`, `absent`)** |
| `restricted` | <center>`bool`</center> | <center>Optional</center> | If true, the User must be granted access to perform actions or access entities on this Account.  **(Default: `True`; Updatable)** |
| `email` | <center>`str`</center> | <center>Optional</center> | The email address for the User. Linode sends emails to this address for account management communications. May be used for other communications as configured.   |
| [`grants` (sub-options)](#grants) | <center>`dict`</center> | <center>Optional</center> | Update the grants a user has.  **(Updatable)** |

### grants

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| [`global` (sub-options)](#global) | <center>`dict`</center> | <center>Optional</center> | A structure containing the Account-level grants a User has.  **(Updatable)** |
| [`resources` (sub-options)](#resources) | <center>`list`</center> | <center>Optional</center> | A list of resource grants to give to the user.  **(Updatable)** |

### global

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `account_access` | <center>`str`</center> | <center>Optional</center> | The level of access this User has to Account-level actions, like billing information. A restricted User will never be able to manage users.  **(Choices: `read_only`, `read_write`; Updatable)** |
| `add_databases` | <center>`bool`</center> | <center>Optional</center> | If true, this User may add Managed Databases.  **(Default: `False`; Updatable)** |
| `add_domains` | <center>`bool`</center> | <center>Optional</center> | If true, this User may add Domains.  **(Default: `False`; Updatable)** |
| `add_firewalls` | <center>`bool`</center> | <center>Optional</center> | If true, this User may add Firewalls.  **(Default: `False`; Updatable)** |
| `add_images` | <center>`bool`</center> | <center>Optional</center> | If true, this User may add Images.  **(Default: `False`; Updatable)** |
| `add_linodes` | <center>`bool`</center> | <center>Optional</center> | If true, this User may add Linodes.  **(Default: `False`; Updatable)** |
| `add_longview` | <center>`bool`</center> | <center>Optional</center> | If true, this User may add Longview.  **(Default: `False`; Updatable)** |
| `add_nodebalancers` | <center>`bool`</center> | <center>Optional</center> | If true, this User may add NodeBalancers.  **(Default: `False`; Updatable)** |
| `add_stackscripts` | <center>`bool`</center> | <center>Optional</center> | If true, this User may add StackScripts.  **(Default: `False`; Updatable)** |
| `add_volumes` | <center>`bool`</center> | <center>Optional</center> | If true, this User may add Volumes.  **(Default: `False`; Updatable)** |
| `cancel_account` | <center>`bool`</center> | <center>Optional</center> | If true, this User may add cancel the entire account.  **(Default: `False`; Updatable)** |
| `longview_subscription` | <center>`bool`</center> | <center>Optional</center> | If true, this User may manage the Account’s Longview subscription.  **(Default: `False`; Updatable)** |

### resources

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `type` | <center>`str`</center> | <center>**Required**</center> | The type of resource to grant access to.  **(Choices: `domain`, `image`, `linode`, `longview`, `nodebalancer`, `stackscript`, `volume`, `database`; Updatable)** |
| `id` | <center>`int`</center> | <center>**Required**</center> | The ID of the resource to grant access to.  **(Updatable)** |
| `permissions` | <center>`str`</center> | <center>**Required**</center> | The level of access this User has to this entity. If null, this User has no access.  **(Choices: `read_only`, `read_write`; Updatable)** |

## Return Values

- `user` - The user in JSON serialized form.

    - Sample Response:
        ```json
        {
          "email": "example_user@linode.com",
          "restricted": true,
          "user_type": "default",
          "ssh_keys": [
            "home-pc",
            "laptop"
          ],
          "tfa_enabled": null,
          "username": "example_user"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-user) for a list of returned fields


- `grants` - The grants info in JSON serialized form.

    - Sample Response:
        ```json
        {
          "domain": [
            {
              "id": 123,
              "label": "example-entity",
              "permissions": "read_only"
            }
          ],
          "global": {
            "account_access": "read_only",
            "add_databases": true,
            "add_domains": true,
            "add_firewalls": true,
            "add_images": true,
            "add_linodes": true,
            "add_longview": true,
            "add_nodebalancers": true,
            "add_stackscripts": true,
            "add_volumes": true,
            "cancel_account": false,
            "longview_subscription": true
          },
          "image": [
            {
              "id": 123,
              "label": "example-entity",
              "permissions": "read_only"
            }
          ],
          "linode": [
            {
              "id": 123,
              "label": "example-entity",
              "permissions": "read_only"
            }
          ],
          "longview": [
            {
              "id": 123,
              "label": "example-entity",
              "permissions": "read_only"
            }
          ],
          "nodebalancer": [
            {
              "id": 123,
              "label": "example-entity",
              "permissions": "read_only"
            }
          ],
          "stackscript": [
            {
              "id": 123,
              "label": "example-entity",
              "permissions": "read_only"
            }
          ],
          "volume": [
            {
              "id": 123,
              "label": "example-entity",
              "permissions": "read_only"
            }
          ]
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-user-grants) for a list of returned fields


