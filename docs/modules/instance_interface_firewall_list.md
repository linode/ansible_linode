# instance_interface_firewall_list

List and filter on Linode Interface Firewalls.

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
- name: List all firewalls under a Linode Interface
  linode.cloud.instance_interface_firewall_list:
    linode_id: 12345
    interface_id: 789
  
```

```yaml
- name: List all firewalls matching the label my-firewall under a Linode Interface
  linode.cloud.instance_interface_firewall_list:
    linode_id: 12345
    interface_id: 789
    filters:
      - name: label
        values: my-firewall
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `linode_id` | <center>`int`</center> | <center>**Required**</center> | The parent Instance for the Linode Interface Firewalls.   |
| `interface_id` | <center>`int`</center> | <center>**Required**</center> | The parent Linode Interface for the Linode Interface Firewalls.   |
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Linode Interface Firewalls in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Linode Interface Firewalls by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Linode Interface Firewalls.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Linode Interface Firewalls to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-linode-interface-firewalls).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `firewalls` - The returned Linode Interface Firewalls.

    - Sample Response:
        ```json
        [
          {
            "created": "2025-01-01T00:01:01",
            "id": 123,
            "label": "firewall123",
            "rules": {
              "inbound": [
                {
                  "action": "ACCEPT",
                  "addresses": {
                    "ipv4": [
                      "192.0.2.0/24",
                      "192.0.2.148/24"
                    ],
                    "ipv6": [
                      "2001:DB8::/128"
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
                      "192.0.2.0/24",
                      "192.0.2.156/24"
                    ],
                    "ipv6": [
                      "2001:DB8::/128"
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
            "updated": "2025-01-02T00:01:01"
          }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-linode-interface-firewalls) for a list of returned fields


