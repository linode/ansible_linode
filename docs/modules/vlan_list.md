# vlan_list

List and filter on Linode VLANs.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: List all of the VLANs for the current Linode Account
  linode.cloud.vlan_list: {}
```

```yaml
- name: List all VLANs in the us-southeast region
  linode.cloud.vlan_list:
    filter:
      - name: region
        values: us-southeast
```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | `str` | Optional | The order to list events in.  (Choices:  `desc`  `asc` Default: `asc`) |
| `order_by` | `str` | Optional | The attribute to order events by.   |
| [`filters` (sub-options)](#filters) | `list` | Optional | A list of filters to apply to the resulting events.   |
| `count` | `int` | Optional | The number of results to return. If undefined, all results will be returned.   |





### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | `str` | **Required** | The name of the field to filter on. Valid filterable attributes can be found here: https://www.linode.com/docs/api/networking/#vlans-list__response-samples   |
| `values` | `list` | **Required** | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |






## Return Values

- `vlan` - The returned VLANs.

    - Sample Response:
        ```json
        [
           {
           "created": "2020-01-01T00:01:01",
            "label": "vlan-example",
            "linodes": [
                111,
                222
              ],
              "region": "ap-west"
           }
        ]
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/networking/#vlans-list__response-samples) for a list of returned fields


