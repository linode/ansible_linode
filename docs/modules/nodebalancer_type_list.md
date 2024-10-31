# nodebalancer_type_list

List and filter on Node Balancer Types.

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
- name: List all of the Linode Node Balancer Types
  linode.cloud.nodebalancer_type_list: {}
```

```yaml
- name: List a Linode Node Balancer Type named NodeBalancer
  linode.cloud.nodebalancer_type_list:
    filters:
      - name: label
        values: NodeBalancer

```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Node Balancer Types in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Node Balancer Types by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Node Balancer Types.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Node Balancer Types to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-node-balancer-types).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `nodebalancer_types` - The returned Node Balancer Types.

    - Sample Response:
        ```json
        [
            {
                "id": "nodebalancer",
                "label": "NodeBalancer",
                "price": {
                    "hourly": 0.015,
                    "monthly": 10.0
                },
                "region_prices": [
                    {
                        "id": "id-cgk",
                        "hourly": 0.018,
                        "monthly": 12.0
                    },
                    {
                        "id": "br-gru",
                        "hourly": 0.021,
                        "monthly": 14.0
                    }
                ],
                "transfer": 0
            }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-node-balancer-types) for a list of returned fields


