"""Documentation fragments for the firewall module"""

specdoc_examples = ['''
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
    state: present''', '''
- name: Delete a Linode Firewall
  linode.cloud.firewall:
    label: 'my-firewall'
    state: absent''']

result_firewall_samples = ['''{
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
}''']

result_devices_samples = ['''[
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
]''']
