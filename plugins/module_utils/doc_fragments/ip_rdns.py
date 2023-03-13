"""Documentation fragments for the ip_rdns module"""

specdoc_examples = ['''
- name: Update reverse DNS
  linode.cloud.ip_rdns:
    state: present
    address: 97.107.143.141
    rdns: 97.107.143.141.nip.io
''',
'''
- name: Remove the reverse DNS
  linode.cloud.ip_rdns:
    state: absent
    address: 97.107.143.141
'''
]
