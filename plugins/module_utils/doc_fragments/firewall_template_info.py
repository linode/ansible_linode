"""Documentation fragments for the firewall_template_info module"""

specdoc_examples = ['''
- name: Get info about a Firewall Template by slug
  linode.cloud.firewall_template_info:
    slug: public''']

result_firewall_template_samples = ['''
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
}''']
