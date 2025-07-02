"""Documentation fragments for the vpc_list module"""

specdoc_examples = ['''
- name: List all firewalls under a Linode Interface
  linode.cloud.instance_interface_firewall_list:
    linode_id: 12345
    interface_id: 789
  ''', '''
- name: List all firewalls matching the label my-firewall under a Linode Interface
  linode.cloud.instance_interface_firewall_list:
    linode_id: 12345
    interface_id: 789
    filters:
      - name: label
        values: my-firewall''']

result_firewalls_samples = {'''[
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
]'''}
