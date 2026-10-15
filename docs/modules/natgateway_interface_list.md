# natgateway_interface_list

List and filter on NAT Gateway Interfaces.

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
- name: List the Interfaces for a NAT Gateway
  linode.cloud.natgateway_interface_list:
    id: 123
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>**Required**</center> | The parent NAT Gateway for the NAT Gateway Interfaces.   |
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list NAT Gateway Interfaces in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order NAT Gateway Interfaces by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting NAT Gateway Interfaces.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of NAT Gateway Interfaces to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-natgateway-interfaces).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `interfaces` - The returned NAT Gateway Interfaces.

    - Sample Response:
        ```json
        [
            {
              "addresses": [
                "203.0.113.42",
                "203.0.113.43"
              ],
              "id": 142,
              "linode": {
                "id": 1001,
                "label": "linode1001",
                "type": "linode",
                "url": "/v4/linode/instances/1001"
              }
            },
            {
              "addresses": [
                "203.0.113.42",
                "203.0.113.43"
              ],
              "id": 143,
              "linode": {
                "id": 1002,
                "label": "linode1002",
                "type": "linode",
                "url": "/v4/linode/instances/1002"
              }
            }
          ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-natgateway-interfaces) for a list of returned fields


