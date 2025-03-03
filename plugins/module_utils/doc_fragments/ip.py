"""Documentation fragments for the ip module"""
specdoc_examples = ['''
- name: Allocate IP to Linode
  linode.cloud.ip:
    linode_id: 123
    public: true
    type: ipv4
    state: present''']

result_ip_samples = ['''{
  "address": "97.107.143.141",
  "gateway": "97.107.143.1",
  "linode_id": 123,
  "prefix": 24,
  "public": true,
  "rdns": "test.example.org",
  "region": "us-east",
  "subnet_mask": "255.255.255.0",
  "type": "ipv4",
  "vpc_nat_1_1": {
    "vpc_id": 242,
    "subnet_id": 194,
    "address": "139.144.244.36"
  }
}''']
