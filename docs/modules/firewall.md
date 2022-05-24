# firewall

Manage Linode Firewalls.


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


- `label` -  The unique label to give this Firewall. 
- `devices` -  The devices that are attached to this Firewall. 
    - `id` - **(Required)** The unique ID of the device to attach to this Firewall. 
    - `type` -  The type of device to be attached to this Firewall. 
- `rules` -  The inbound and outbound access rules to apply to this Firewall. 
    - `inbound` -  A list of rules for inbound traffic. 
        - `label` - **(Required)** The label of this rule. 
        - `action` - **(Required)** Controls whether traffic is accepted or dropped by this rule. 
        - `addresses` -  Allowed IPv4 or IPv6 addresses. 
            - `ipv4` -  A list of IPv4 addresses or networks. Must be in IP/mask format. 
            - `ipv6` -  A list of IPv4 addresses or networks. Must be in IP/mask format. 
        - `description` -  A description for this rule. 
        - `ports` -  A string representing the port or ports on which traffic will be allowed. See U(https://www.linode.com/docs/api/networking/#firewall-create) 
        - `protocol` -  The type of network traffic to allow. 
    - `inbound_policy` -  The default behavior for inbound traffic. 
    - `outbound` -  A list of rules for outbound traffic. 
        - `label` - **(Required)** The label of this rule. 
        - `action` - **(Required)** Controls whether traffic is accepted or dropped by this rule. 
        - `addresses` -  Allowed IPv4 or IPv6 addresses. 
            - `ipv4` -  A list of IPv4 addresses or networks. Must be in IP/mask format. 
            - `ipv6` -  A list of IPv4 addresses or networks. Must be in IP/mask format. 
        - `description` -  A description for this rule. 
        - `ports` -  A string representing the port or ports on which traffic will be allowed. See U(https://www.linode.com/docs/api/networking/#firewall-create) 
        - `protocol` -  The type of network traffic to allow. 
    - `outbound_policy` -  The default behavior for outbound traffic. 
- `status` -  The status of this Firewall. 


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
    - See the [Linode API response documentation](https://www.linode.com/docs/api/networking/#firewall-view) for a list of returned fields


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
    - See the [Linode API response documentation](https://www.linode.com/docs/api/networking/#firewall-device-view) for a list of returned fields


