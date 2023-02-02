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
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Instance Types in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Instance Types by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Instance Types.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of results to return. If undefined, all results will be returned.   |





### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable attributes can be found here: https://www.linode.com/docs/api/linode-types/#types-list__response-samples   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |






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


