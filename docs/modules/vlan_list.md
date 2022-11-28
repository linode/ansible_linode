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
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list VLANs in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order VLANs by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting VLANs.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of results to return. If undefined, all results will be returned.   |





### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable attributes can be found here: https://www.linode.com/docs/api/networking/#vlans-list__response-samples   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |






## Return Values

- `vlans` - The returned VLANs.

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


