# vlan_info

Get info about a Linode VLAN.


## Examples

```yaml
- name: Get info about a VLAN by label
  linode.cloud.vlan_info:
    label: example-vlan
```


## Parameters



- `label` (`str`) - **(Required)** The VLAN’s label.  


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


