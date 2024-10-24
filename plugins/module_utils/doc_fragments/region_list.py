"""Documentation fragments for the region_list module"""

specdoc_examples = ['''
- name: List all of the Linode regions
  linode.cloud.region_list: {}''', '''
- name: Filtered Linode regions
  linode.cloud.region_list:
    filters:
      - name: site_type
        values: core''']

result_regions_samples = ['''[
    {
      "capabilities": [
        "Linodes",
        "Backups",
        "NodeBalancers",
        "Block Storage",
        "Object Storage",
        "Kubernetes",
        "Cloud Firewall",
        "Vlans",
        "VPCs",
        "Metadata",
        "Premium Plans"
      ],
      "country": "us",
      "id": "us-mia",
      "label": "Miami, FL",
      "resolvers": {
        "ipv4": "172.233.160.34, 172.233.160.27",
        "ipv6": "2a01:7e04::f03c:93ff:fead:d31f, 2a01:7e04::f03c:93ff:fead:d37f"
      },
      "site_type": "core",
      "status": "ok"
    }
]''']
