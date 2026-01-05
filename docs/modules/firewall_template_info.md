# firewall_template_info

Get info about a Linode Firewall Template.

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
- name: Get info about a Firewall Template by slug
  linode.cloud.firewall_template_info:
    slug: public
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `slug` | <center>`str`</center> | <center>**Required**</center> | The Slug of the Firewall Template to resolve.   |

## Return Values

- `firewall_template` - The returned Firewall Template.

    - Sample Response:
        ```json
        
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
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-firewall-template) for a list of returned fields


