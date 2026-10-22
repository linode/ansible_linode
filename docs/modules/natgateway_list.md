# natgateway_list

List and filter on NAT Gateways.

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
- name: List all of the NAT Gateways for the current Linode Account
  linode.cloud.natgateway_list: {}
```

```yaml
- name: List the latest 5 NAT Gateways for the current Linode Account
  linode.cloud.natgateway_list:
    count: 5
    order_by: created
    order: desc
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list NAT Gateways in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order NAT Gateways by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting NAT Gateways.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of NAT Gateways to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-natgateways).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `natgateways` - The returned NAT Gateways.

    - Sample Response:
        ```json
        [
            {
              "address_autoscale_max": 0,
              "addresses": [
                {
                  "address": "203.0.113.42"
                },
                {
                  "address": "203.0.113.43"
                }
              ],
              "created": "2026-01-01T00:01:01",
              "default_ports_per_interface": 4096,
              "id": 42,
              "label": "reserved-ips-natgateway",
              "portset_assignments": 0,
              "portset_capacity": 65536,
              "region": "gb-lon",
              "updated": "2026-03-01T00:01:01",
              "vpc_subnet": {
                "id": 42,
                "label": "my-subnet",
                "vpc_id": 13,
                "vpc_label": "my-vpc"
              }
            },
            {
              "address_autoscale_max": 4,
              "addresses": [
                {
                  "address": "203.0.113.44"
                }
              ],
              "created": "2026-01-02T00:01:01",
              "default_ports_per_interface": 4096,
              "id": 43,
              "label": "autoscale-natgateway",
              "portset_assignments": 12,
              "portset_capacity": 32768,
              "region": "gb-lon",
              "updated": "2026-03-01T00:01:01",
              "vpc_subnet": null
            }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-natgateways) for a list of returned fields


