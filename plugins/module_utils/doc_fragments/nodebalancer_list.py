"""Documentation fragments for the nodebalancer_list module"""

specdoc_examples = ['''
- name: List all of the Nodebalancers for the current Linode Account
  linode.cloud.nodebalancer_list: {}''', '''
- name: Resolve all Nodebalancers for the current Linode Account
  linode.cloud.nodebalancer_list:
    filters:
      - name: label
        values: myNodebalancerLabel''']

result_nodebalancers_samples = ['''[
    {
      "client_conn_throttle": 0,
      "created": "2018-01-01T00:01:01",
      "hostname": "192.0.2.1.ip.linodeusercontent.com",
      "id": 12345,
      "ipv4": "203.0.113.1",
      "ipv6": null,
      "label": "balancer12345",
      "region": "us-east",
      "tags": [
        "example tag",
        "another example"
      ],
      "transfer": {
        "in": 28.91200828552246,
        "out": 3.5487728118896484,
        "total": 32.46078109741211
      },
      "updated": "2018-03-01T00:01:01"
    }
]''']
