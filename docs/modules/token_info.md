# token_info

Get info about a Linode Personal Access Token.

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
- name: Get info about a token by label
  linode.cloud.token_info:
    label: my-token
```

```yaml
- name: Get info about a token by ID
  linode.cloud.token_info:
    id: 12345
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the Personal Access Token to resolve.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the Personal Access Token to resolve.  **(Conflicts With: `id`)** |

## Return Values

- `token` - The returned Personal Access Token.

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
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-personal-access-tokens) for a list of returned fields


