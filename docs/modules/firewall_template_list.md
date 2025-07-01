# firewall_template_list

List and filter on Firewall Templates.

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
- name: List all of the firewall templates
  linode.cloud.firewall_template_list: {}
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Firewall Templates in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Firewall Templates by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Firewall Templates.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Firewall Templates to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-firewall-templates).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `firewall_templates` - The returned Firewall Templates.

    - Sample Response:
        ```json
        
        [
          {
            "rules": {
              "inbound": [
                {
                  "action": "ACCEPT",
                  "addresses": {
                    "ipv4": [
                      "0.0.0.0/0"
                    ],
                    "ipv6": [
                      "::/0"
                    ]
                  },
                  "description": "Accept inbound SSH",
                  "label": "accept-inbound-ssh",
                  "ports": "22",
                  "protocol": "TCP"
                },
                {
                  "action": "ACCEPT",
                  "addresses": {
                    "ipv4": [
                      "0.0.0.0/0"
                    ],
                    "ipv6": [
                      "::/0"
                    ]
                  },
                  "description": "Accept inbound ICMP",
                  "label": "accept-inbound-icmp",
                  "protocol": "ICMP"
                },
                {
                  "action": "ACCEPT",
                  "addresses": {
                    "ipv4": [
                      "10.0.0.0/8",
                      "192.168.0.0/17",
                      "172.16.0.0/12"
                    ]
                  },
                  "description": "Accept inbound RFC-1918",
                  "label": "accept-inbound-rfc1918",
                  "ports": "1-65535",
                  "protocol": "TCP"
                },
                {
                  "action": "ACCEPT",
                  "addresses": {
                    "ipv4": [
                      "10.0.0.0/8",
                      "192.168.0.0/17",
                      "172.16.0.0/12"
                    ]
                  },
                  "description": "Accept inbound RFC-1918",
                  "label": "accept-inbound-rfc1918",
                  "ports": "1-65535",
                  "protocol": "UDP"
                }
              ],
              "inbound_policy": "DROP",
              "outbound": [],
              "outbound_policy": "ACCEPT"
            },
            "slug": "vpc"
          },
          {
            "rules": {
              "inbound": [
                {
                  "action": "ACCEPT",
                  "addresses": {
                    "ipv4": [
                      "0.0.0.0/0"
                    ],
                    "ipv6": [
                      "::/0"
                    ]
                  },
                  "description": "Accept inbound SSH",
                  "label": "accept-inbound-ssh",
                  "ports": "22",
                  "protocol": "TCP"
                },
                {
                  "action": "ACCEPT",
                  "addresses": {
                    "ipv4": [
                      "0.0.0.0/0"
                    ],
                    "ipv6": [
                      "::/0"
                    ]
                  },
                  "description": "Accept inbound ICMP",
                  "label": "accept-inbound-icmp",
                  "protocol": "ICMP"
                }
              ],
              "inbound_policy": "DROP",
              "outbound": [],
              "outbound_policy": "ACCEPT"
            },
            "slug": "public"
          }
        ]
        
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-firewall-templates) for a list of returned fields


