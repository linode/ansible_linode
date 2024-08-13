# user_info

Get info about a Linode User.

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
- name: Get info about a user
  linode.cloud.user_info:
    username: my-cool-user
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `username` | <center>`str`</center> | <center>**Required**</center> | The Username of the User to resolve.   |

## Return Values

- `user` - The returned User.

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


- `grants` - The returned Grants.

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


