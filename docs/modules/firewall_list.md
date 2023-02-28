# firewall_list

List and filter on Firewalls.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: List all of the accessible firewalls for the current Linode Account
  linode.cloud.firewall_list: {}
```

```yaml
- name: Resolve all accessible firewall for the current Linode Account
  linode.cloud.firewall_list:
    filter:
      - name: label
        values: myFirewallLabel
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list firewalls in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order firewalls by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting firewalls.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of results to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable attributes can be found here: https://www.linode.com/docs/api/networking/#firewalls-list__responses   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `firewalls` - The returned firewalls.

    - Sample Response:
        ```json
        [
            {
              "created": "2018-01-01T00:01:01",
              "id": 123,
              "label": "firewall123",
              "rules": {
                "inbound": [
                  {
                    "action": "ACCEPT",
                    "addresses": {
                      "ipv4": [
                        "192.0.2.0/24"
                      ],
                      "ipv6": [
                        "2001:DB8::/32"
                      ]
                    },
                    "description": "An example firewall rule description.",
                    "label": "firewallrule123",
                    "ports": "22-24, 80, 443",
                    "protocol": "TCP"
                  }
                ],
                "inbound_policy": "DROP",
                "outbound": [
                  {
                    "action": "ACCEPT",
                    "addresses": {
                      "ipv4": [
                        "192.0.2.0/24"
                      ],
                      "ipv6": [
                        "2001:DB8::/32"
                      ]
                    },
                    "description": "An example firewall rule description.",
                    "label": "firewallrule123",
                    "ports": "22-24, 80, 443",
                    "protocol": "TCP"
                  }
                ],
                "outbound_policy": "DROP"
              },
              "status": "enabled",
              "tags": [
                "example tag",
                "another example"
              ],
              "updated": "2018-01-02T00:01:01"
            }
        ]
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/networking/#firewalls-list__response-samples) for a list of returned fields


