"""Documentation fragments for the ip_assign module"""
specdoc_examples = ['''
- name: Assign IP to Linode
  linode.cloud.ip_assign:
    region: us-east
    assignments:
     - address: 0.0.0.0
       linode_id: 123''']

result_ip_assign_samples = ['''[{}]''']
