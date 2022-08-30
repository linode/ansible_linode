# token

Manage a Linode Token.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

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
    domain: my-token
    state: absent
```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | `str` | **Required** | This token's unique label.   |
| `state` | `str` | **Required** | The state of this token.  (Choices:  `present`  `absent` ) |
| `expiry` | `str` | Optional | When this token should be valid until.   |
| `scopes` | `str` | Optional | The OAuth scopes to create the token with.   |






## Return Values

- `volume` - The token in JSON serialized form.

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
    - See the [Linode API response documentation](https://www.linode.com/docs/api/profile/#personal-access-token-create__responses) for a list of returned fields


