# lke_type_list

List and filter on LKE Types.

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
- name: List all of the Linode LKE Types
  linode.cloud.lke_type_list: {}
```

```yaml
- name: List a Linode LKE Type named LKE High Availability
  linode.cloud.lke_type_list:
    filters:
      - name: label
        values: LKE High Availability

```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list LKE Types in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order LKE Types by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting LKE Types.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of LKE Types to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-lke-types).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `lke_types` - The returned LKE Types.

    - Sample Response:
        ```json
        [
            {
                "id": "lke-ha",
                "label": "LKE High Availability",
                "price": {
                    "hourly": 0.09,
                    "monthly": 60.0
                },
                "region_prices": [
                    {
                        "id": "id-cgk",
                        "hourly": 0.108,
                        "monthly": 72.0
                    },
                    {
                        "id": "br-gru",
                        "hourly": 0.126,
                        "monthly": 84.0
                    }
                ],
                "transfer": 0
            }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-lke-types) for a list of returned fields


