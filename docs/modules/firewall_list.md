# firewall_list

List and filter on Firewalls.

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
- name: List all of the accessible firewalls for the current Linode Account
  linode.cloud.firewall_list: {}
```

```yaml
- name: Resolve all accessible firewall for the current Linode Account
  linode.cloud.firewall_list:
    filters:
      - name: label
        values: myFirewallLabel
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Firewalls in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Firewalls by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Firewalls.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Firewalls to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-firewalls).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `firewalls` - The returned Firewalls.

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
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-firewalls) for a list of returned fields


