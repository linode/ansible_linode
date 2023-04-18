"""Documentation fragments for the domain_list module"""

specdoc_examples = ['''
- name: List all of the domains for the current Linode Account
  linode.cloud.domain_list: {}''', '''
- name: Resolve all domains for the current Linode Account
  linode.cloud.domain_list:
    filters:
      - name: domain
        values: example.org''']

result_domains_samples = ['''[
    {
      "axfr_ips": [],
      "description": null,
      "domain": "example.org",
      "expire_sec": 300,
      "group": null,
      "id": 1234,
      "master_ips": [],
      "refresh_sec": 300,
      "retry_sec": 300,
      "soa_email": "admin@example.org",
      "status": "active",
      "tags": [
        "example tag",
        "another example"
      ],
      "ttl_sec": 300,
      "type": "master"
    }
]''']
