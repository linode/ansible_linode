"""Documentation fragments for the ip module"""
specdoc_examples = ['''
- name: Allocate IP to Linode
  linode.cloud.ip:
    linode_id: 123
    public: true
    type: ipv4''']

result_ip_samples = ['''[{}]''']
