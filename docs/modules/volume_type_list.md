# volume_type_list

List and filter on Volume Types.

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
- name: List all of the Linode Volume Types
  linode.cloud.volume_type_list: {}
```

```yaml
- name: List a Linode Volume Type named Storage Volume
  linode.cloud.volume_type_list:
    filters:
      - name: label
        values: Storage Volume

```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Volume Types in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Volume Types by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Volume Types.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Volume Types to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-volume-types).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `volume_types` - The returned Volume Types.

    - Sample Response:
        ```json
        [
            {
                "id": "volume",
                "label": "Storage Volume",
                "price": {
                    "hourly": 0.00015,
                    "monthly": 0.1
                },
                "region_prices": [
                    {
                        "id": "id-cgk",
                        "hourly": 0.00018,
                        "monthly": 0.12
                    },
                    {
                        "id": "br-gru",
                        "hourly": 0.00021,
                        "monthly": 0.14
                    }
                ],
                "transfer": 0
            }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-volume-types) for a list of returned fields


