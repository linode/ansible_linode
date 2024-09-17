# firewall_info

Get info about a Linode Firewall.

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
- name: Get info about a Firewall by label
  linode.cloud.firewall_info:
    label: 'my-firewall' 
```

```yaml
- name: Get info about a Firewall by id
  linode.cloud.firewall_info:
    id: 12345
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the Firewall to resolve.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the Firewall to resolve.  **(Conflicts With: `id`)** |

## Return Values

- `firewall` - The returned Firewall.

    - Sample Response:
        ```json
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
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-firewall) for a list of returned fields


- `devices` - The returned devices.

    - Sample Response:
        ```json
        [
          {
            "created": "2018-01-01T00:01:01",
            "entity": {
              "id": 123,
              "label": "my-linode",
              "type": "linode",
              "url": "/v4/linode/instances/123"
            },
            "id": 123,
            "updated": "2018-01-02T00:01:01"
          }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-firewall-devices) for a list of returned fields


