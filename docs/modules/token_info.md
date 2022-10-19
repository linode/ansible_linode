# token_info

Get info about a Linode Personal Access Token.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

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
| `id` | `int` | Optional | The ID of the token.   |
| `label` | `str` | Optional | The label of the token.   |






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
    - See the [Linode API response documentation](https://www.linode.com/docs/api/profile/#personal-access-token-create__response-samples) for a list of returned fields


