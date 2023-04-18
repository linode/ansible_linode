"""Documentation fragments for the firewall_list module"""

specdoc_examples = ['''
- name: List all of the accessible firewalls for the current Linode Account
  linode.cloud.firewall_list: {}''', '''
- name: Resolve all accessible firewall for the current Linode Account
  linode.cloud.firewall_list:
    filters:
      - name: label
        values: myFirewallLabel''']

result_firewalls_samples = ['''[
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
]''']
