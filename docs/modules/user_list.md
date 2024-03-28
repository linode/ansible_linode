# user_list

List Users.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: List all of the users for the current Linode Account
  linode.cloud.user_list: {}
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list users in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of results to return. If undefined, all results will be returned.   |

## Return Values

- `users` - The returned users.

    - Sample Response:
        ```json
        [
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
        ]
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/account/#users-list__response-samples) for a list of returned fields


