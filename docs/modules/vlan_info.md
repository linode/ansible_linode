# vlan_info

Get info about a Linode VLAN.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Get info about a VLAN by label
  linode.cloud.vlan_info:
    label: example-vlan
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | <center>`str`</center> | <center>**Required**</center> | The VLAN’s label.   |
| `api_token` | <center>`str`</center> | <center>Optional</center> | The Linode account personal access token. It is necessary to run the module. It can be exposed by the environment variable `LINODE_API_TOKEN` instead.   |

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


