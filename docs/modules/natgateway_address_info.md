# natgateway_address_info

Get info about a Linode NAT Gateway Address.

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
- name: Get info about a NAT Gateway Address
  linode.cloud.natgateway_address_info:
    id: 123
    address: 100.123.97.131 
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>**Required**</center> | The ID of the NAT Gateway.   |
| `address` | <center>`str`</center> | <center>**Required**</center> | The address to retrieve information about.   |

## Return Values

- `address` - The NAT Gateway Address in JSON serialized form.

    - Sample Response:
        ```json
        {
          "address": "203.0.113.43",
          "in_use": true,
          "interface_count": 6,
          "portset_assignments": 6,
          "portset_capacity": 63
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-natgateway-address) for a list of returned fields


