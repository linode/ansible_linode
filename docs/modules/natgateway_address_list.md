# natgateway_address_list

List and filter on NAT Gateway Addresses.

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
- name: List the addresses for a NAT Gateway
  linode.cloud.natgateway_address_list:
    id: 123
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>**Required**</center> | The parent NAT Gateway for the NAT Gateway Addresses.   |
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list NAT Gateway Addresses in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order NAT Gateway Addresses by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting NAT Gateway Addresses.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of NAT Gateway Addresses to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-natgateways).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `addresses` - The returned NAT Gateway Addresses.

    - Sample Response:
        ```json
        [
            {
              "address": "203.0.113.43",
              "in_use": true,
              "interface_count": 6,
              "portset_assignments": 6,
              "portset_capacity": 63
            },
            {
              "address": "203.0.113.44",
              "in_use": false,
              "interface_count": 0,
              "portset_assignments": 0,
              "portset_capacity": 63
            }
          ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-natgateways) for a list of returned fields


