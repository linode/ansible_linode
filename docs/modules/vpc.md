# vpc

Create, read, and update a Linode VPC.

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
| `label` | <center>`str`</center> | <center>**Required**</center> | This VPC's unique label.   |
| `state` | <center>`str`</center> | <center>**Required**</center> | The state of this token.  **(Choices: `present`, `absent`)** |
| `description` | <center>`str`</center> | <center>Optional</center> | A description describing this VPC.   |
| `region` | <center>`str`</center> | <center>Optional</center> | The region this VPC is located in.   |

## Return Values

- `vpc` - The VPC in JSON serialized form.

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
    - See the [Linode API response documentation](TODO) for a list of returned fields


