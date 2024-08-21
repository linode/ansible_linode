"""Documentation fragments for the ip_share module"""
specdoc_examples = ['''
- name: Configure the Linode shared IPs.
  linode.cloud.ip_share:
    api_version: v4beta
    linode_id: 12345
    ips: ["192.0.2.1", "2001:db8:3c4d:15::"]''']

result_ip_share_stats_samples = ['''[
  {
    "linode_id": 12345,
    "ips": ["192.0.2.1", "2001:db8:3c4d:15::"]
  }
]''']
