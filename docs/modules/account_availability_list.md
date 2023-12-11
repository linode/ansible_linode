# account_availability_list

List Account Availabilities. No filter can be sent to the API currently. Only count is definable.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: List all of the region resource availabilities to the account
  linode.cloud.account_availability_list: {}
```

```yaml
- name: List 5 regions' availabilities to the Linode Account
  linode.cloud.account_availability_list:
    count: 5
```


## Parameters

| Field     | Type | Required | Description                                                                                 |
|-----------|------|----------|---------------------------------------------------------------------------------------------|
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Account Availabilities to return. If undefined, all results will be returned. |


## Return Values

- `account_availabilities` - The returned Account Availabilities.

    - Sample Response:
        ```json
        [
            {
              "region": "ap-west",
              "unavailable": ["Linode"]
            },
            {
              "region": "ca-central",
              "unavailable": ["Linode", "Block Storage"]
            }
        ]
        ```
    - See the [Linode API response documentation](TBD) for a list of returned fields


