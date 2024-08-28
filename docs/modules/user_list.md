# user_list

List and filter on Users.

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
- name: List all of the users for the current Linode Account
  linode.cloud.user_list: {}
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Users in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Users by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Users.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Users to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-users).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `users` - The returned Users.

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
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-users) for a list of returned fields


