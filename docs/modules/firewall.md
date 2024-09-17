# firewall

Manage Linode Firewalls.

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
- name: Create a Linode Firewall
  linode.cloud.firewall:
    label: 'my-firewall'
    devices:
      - id: 123
        type: linode
    rules:
      inbound_policy: DROP
      inbound:
        - label: allow-http-in
          addresses:
            ipv4:
              - 0.0.0.0/0
            ipv6:
              - 'ff00::/8'
          description: Allow inbound HTTP and HTTPS connections.
          ports: '80,443'
          protocol: TCP
          action: ACCEPT

      outbound_policy: DROP
      outbound:
        - label: allow-http-out
          addresses:
            ipv4:
              - 0.0.0.0/0
            ipv6:
              - 'ff00::/8'
          description: Allow outbound HTTP and HTTPS connections.
          ports: '80,443'
          protocol: TCP
          action: ACCEPT
    state: present
```

```yaml
- name: Delete a Linode Firewall
  linode.cloud.firewall:
    label: 'my-firewall'
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the target.  **(Choices: `present`, `absent`, `update`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The unique label to give this Firewall.   |
| [`devices` (sub-options)](#devices) | <center>`list`</center> | <center>Optional</center> | The devices that are attached to this Firewall.  **(Updatable)** |
| [`rules` (sub-options)](#rules) | <center>`dict`</center> | <center>Optional</center> | The inbound and outbound access rules to apply to this Firewall.  **(Updatable)** |
| `status` | <center>`str`</center> | <center>Optional</center> | The status of this Firewall.  **(Updatable)** |
| `tags` | <center>`list`</center> | <center>Optional</center> | A list of tags to apply to this Firewall.  **(Updatable)** |

### devices

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>**Required**</center> | The unique ID of the device to attach to this Firewall.   |
| `type` | <center>`str`</center> | <center>Optional</center> | The type of device to be attached to this Firewall.  **(Default: `linode`)** |

### rules

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| [`inbound` (sub-options)](#inbound) | <center>`list`</center> | <center>Optional</center> | A list of rules for inbound traffic.   |
| `inbound_policy` | <center>`str`</center> | <center>Optional</center> | The default behavior for inbound traffic.   |
| [`outbound` (sub-options)](#outbound) | <center>`list`</center> | <center>Optional</center> | A list of rules for outbound traffic.   |
| `outbound_policy` | <center>`str`</center> | <center>Optional</center> | The default behavior for outbound traffic.   |

### inbound

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | <center>`str`</center> | <center>**Required**</center> | The label of this rule.   |
| `action` | <center>`str`</center> | <center>**Required**</center> | Controls whether traffic is accepted or dropped by this rule.  **(Choices: `ACCEPT`, `DROP`)** |
| [`addresses` (sub-options)](#addresses) | <center>`dict`</center> | <center>Optional</center> | Allowed IPv4 or IPv6 addresses.   |
| `description` | <center>`str`</center> | <center>Optional</center> | A description for this rule.   |
| `ports` | <center>`str`</center> | <center>Optional</center> | A string representing the port or ports on which traffic will be allowed. See https://techdocs.akamai.com/linode-api/reference/post-firewalls   |
| `protocol` | <center>`str`</center> | <center>Optional</center> | The type of network traffic to allow.   |

### addresses

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `ipv4` | <center>`list`</center> | <center>Optional</center> | A list of IPv4 addresses or networks. Must be in IP/mask format.   |
| `ipv6` | <center>`list`</center> | <center>Optional</center> | A list of IPv6 addresses or networks. Must be in IP/mask format.   |

### outbound

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | <center>`str`</center> | <center>**Required**</center> | The label of this rule.   |
| `action` | <center>`str`</center> | <center>**Required**</center> | Controls whether traffic is accepted or dropped by this rule.  **(Choices: `ACCEPT`, `DROP`)** |
| [`addresses` (sub-options)](#addresses) | <center>`dict`</center> | <center>Optional</center> | Allowed IPv4 or IPv6 addresses.   |
| `description` | <center>`str`</center> | <center>Optional</center> | A description for this rule.   |
| `ports` | <center>`str`</center> | <center>Optional</center> | A string representing the port or ports on which traffic will be allowed. See https://techdocs.akamai.com/linode-api/reference/post-firewalls   |
| `protocol` | <center>`str`</center> | <center>Optional</center> | The type of network traffic to allow.   |

## Return Values

- `firewall` - The Firewall description in JSON serialized form.

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


- `devices` - A list of Firewall devices JSON serialized form.

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
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-firewall-device) for a list of returned fields


