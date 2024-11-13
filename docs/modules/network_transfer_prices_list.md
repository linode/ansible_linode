# network_transfer_prices_list

List and filter on Network Transfer Prices.

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
- name: List all of the Linode Network Transfer Prices
  linode.cloud.network_transfer_prices_list: {}
```

```yaml
- name: List a Linode Network Transfer Price named Distributed Network Transfer
  linode.cloud.network_transfer_prices_list:
    filters:
      - name: label
        values: Distributed Network Transfer

```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Network Transfer Prices in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Network Transfer Prices by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Network Transfer Prices.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Network Transfer Prices to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-network-transfer-prices).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `network_transfer_prices` - The returned Network Transfer Prices.

    - Sample Response:
        ```json
        [
            {
                "id": "distributed_network_transfer",
                "label": "Distributed Network Transfer",
                "price": {
                    "hourly": 0.01,
                    "monthly": null
                },
                "region_prices": [],
                "transfer": 0
            }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-network-transfer-prices) for a list of returned fields


