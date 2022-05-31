"""Documentation fragments for the domain_info module"""

specdoc_examples = ['''
- name: Get info about a domain by domain
  linode.cloud.domain_info:
    domain: my-domain.com''', '''
- name: Get info about a domain by id
  linode.cloud.domain_info:
    id: 12345''']
