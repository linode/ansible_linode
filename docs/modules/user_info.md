# user_info

Get info about a Linode User.

LINODE_API_TOKEN environment variable is required.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Get info about a user
  linode.cloud.user_info:
    username: my-cool-user
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `username` | <center>`str`</center> | <center>**Required**</center> | The username of the user.   |

## Return Values

- `user` - The user info in JSON serialized form.

    - Sample Response:
        ```json
        {
          "email": "example_user@linode.com",
          "restricted": true,
          "ssh_keys": [
            "home-pc",
            "laptop"
          ],
          "tfa_enabled": null,
          "username": "example_user"
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/account/#user-view) for a list of returned fields


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
    - See the [Linode API response documentation](https://www.linode.com/docs/api/account/#users-grants-view__response-samples) for a list of returned fields


