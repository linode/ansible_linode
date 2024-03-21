# token_list

List and filter on Linode Account tokens.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: List all of the Personal Access Tokens active for the current user
  linode.cloud.token_list: {}
```

```yaml
- name: Resolve all of the Personal Access Tokens active for the current user
  linode.cloud.token_list:
    filters:
      - name: label
        values: myTokenLabel
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list tokens in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order tokens by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting tokens.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of results to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable attributes can be found here: https://www.linode.com/docs/api/profile/#personal-access-tokens-list__responses   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `tokens` - The returned tokens.

    - Sample Response:
        ```json
        [
            {
              "created": "2018-01-01T00:01:01",
              "expiry": "2018-01-01T13:46:32",
              "id": 123,
              "label": "linode-cli",
              "scopes": "*",
              "token": "abcdefghijklmnop"
            }
        ]
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/profile/#personal-access-tokens-list__response-samples) for a list of returned fields


