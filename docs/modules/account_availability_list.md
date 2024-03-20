# account_availability_list

List and filter on Account Availabilitys.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: List all of the region resource availabilities to the account
  linode.cloud.account_availability_list: {}
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `api_token` | <center>`str`</center> | <center>Optional</center> | The Linode account personal access token. It is necessary to run the module. It can be exposed by the environment variable `LINODE_API_TOKEN` instead.   |
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Account Availabilitys in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Account Availabilitys by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Account Availabilitys.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Account Availabilitys to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](TBD).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `account_availabilities` - The returned Account Availabilitys.

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


