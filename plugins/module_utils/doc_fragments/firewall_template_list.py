"""Documentation fragments for the firewall_template_list module"""

specdoc_examples = ['''
- name: List all of the firewall templates
  linode.cloud.firewall_template_list: {}''']

result_firewall_templates_samples = ['''
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
''']
