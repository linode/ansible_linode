# token

Manage a Linode Token.

NOTE: The full Personal Access Token is only returned when a new token has been created.

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
- name: Create a simple token 
  linode.cloud.token:
    label: my-token
    state: present
```

```yaml
- name: Create a token with expiry date and scopes 
  linode.cloud.token:
    label: my-token
    expiry: 2022-07-09T16:59:26
    scope: '*'
    state: present
```

```yaml
- name: Delete a token
  linode.cloud.token:
    label: my-token
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | <center>`str`</center> | <center>**Required**</center> | This token's unique label.   |
| `state` | <center>`str`</center> | <center>**Required**</center> | The state of this token.  **(Choices: `present`, `absent`)** |
| `expiry` | <center>`str`</center> | <center>Optional</center> | When this token should be valid until.   |
| `scopes` | <center>`str`</center> | <center>Optional</center> | The OAuth scopes to create the token with.   |

## Return Values

- `token` - The token in JSON serialized form.

    - Sample Response:
        ```json
        {
          "created": "2018-01-01T00:01:01",
          "expiry": "2018-01-01T13:46:32",
          "id": 123,
          "label": "linode-cli",
          "scopes": "*",
          "token": "abcdefghijklmnop"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/post-personal-access-token) for a list of returned fields


