# vlan_info

Get info about a Linode VLAN.

**:warning: This module makes use of beta endpoints and requires the `api_version` field be explicitly set to `v4beta`.**

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Get info about a VLAN by label
  linode.cloud.vlan_info:
    api_version: v4beta
    label: example-vlan
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | <center>`str`</center> | <center>**Required**</center> | The VLAN’s label.   |

## Return Values

- `vlan` - The VLAN in JSON serialized form.

    - Sample Response:
        ```json
        {
          "created": "2020-01-01T00:01:01",
          "label": "vlan-example",
          "linodes": [
            111,
            222
          ],
          "region": "ap-west"
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/networking/#vlans-list__response-samples) for a list of returned fields


