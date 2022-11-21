# type_list

List and filter on Linode Instance Types.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: List all of the Linode Instance Types
  linode.cloud.type_list: {}
```

```yaml
- name: List a Linode Instance Type named Nanode 1GB
  linode.cloud.type_list:
    filter:
      - name: label
        values: Nanode 1GB

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | `str` | Optional | The order to list Instance Types in.  (Choices:  `desc`  `asc` Default: `asc`) |
| `order_by` | `str` | Optional | The attribute to order Instance Types by.   |
| [`filters` (sub-options)](#filters) | `list` | Optional | A list of filters to apply to the resulting Instance Types.   |
| `count` | `int` | Optional | The number of results to return. If undefined, all results will be returned.   |





### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | `str` | **Required** | The name of the field to filter on. Valid filterable attributes can be found here: https://www.linode.com/docs/api/linode-types/#types-list__response-samples   |
| `values` | `list` | **Required** | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |






## Return Values

- `types` - The returned Instance Types.

    - Sample Response:
        ```json
        [
            {
                "addons": {
                    "backups": {
                        "price": {
                            "hourly": 0.008,
                            "monthly": 5
                        }
                    }
                },
                "class": "standard",
                "disk": 81920,
                "gpus": 0,
                "id": "g6-standard-2",
                "label": "Linode 4GB",
                "memory": 4096,
                "network_out": 1000,
                "price": {
                    "hourly": 0.03,
                    "monthly": 20
                },
                "successor": null,
                "transfer": 4000,
                "vcpus": 2
            }
        ]
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/linode-types/#types-list__response-samples) for a list of returned fields


