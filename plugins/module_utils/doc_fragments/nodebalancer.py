"""Documentation fragments for the nodebalanacer module"""

specdoc_examples = ['''
- name: Create a Linode NodeBalancer
  linode.cloud.nodebalancer:
    label: my-loadbalancer
    region: us-east
    tags: [ prod-env ]
    state: present
    configs:
      - port: 80
        protocol: http
        algorithm: roundrobin
        nodes:
          - label: node1
            address: 0.0.0.0:80''', '''
- name: Delete the NodeBalancer
  linode.cloud.nodebalancer:
    label: my-loadbalancer
    region: us-east
    state: absent''']

result_node_balancer_samples = ['''{
  "client_conn_throttle": 0,
  "created": "2018-01-01T00:01:01",
  "hostname": "192.0.2.1.ip.linodeusercontent.com",
  "id": 12345,
  "ipv4": "12.34.56.78",
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
}''']

result_configs_samples = ['''[
  {
    "algorithm": "roundrobin",
    "check": "http_body",
    "check_attempts": 3,
    "check_body": "it works",
    "check_interval": 90,
    "check_passive": true,
    "check_path": "/test",
    "check_timeout": 10,
    "cipher_suite": "recommended",
    "id": 4567,
    "nodebalancer_id": 12345,
    "nodes_status": {
      "down": 0,
      "up": 4
    },
    "port": 80,
    "protocol": "http",
    "proxy_protocol": "none",
    "ssl_cert": null,
    "ssl_commonname": null,
    "ssl_fingerprint": null,
    "ssl_key": null,
    "stickiness": "http_cookie"
  }
]''']

result_nodes_samples = ['''[
  {
    "address": "192.168.210.120:80",
    "config_id": 4567,
    "id": 54321,
    "label": "node54321",
    "mode": "accept",
    "nodebalancer_id": 12345,
    "status": "UP",
    "weight": 50
  }
]''']

result_firewalls_samples = ['''[
  1234,
  5678
]''']

result_firewalls_data_samples = ['''[
  {
    "created": "2020-04-10T13:34:00",
    "entities": [
      {
        "id": 1234,
        "label": "example-label",
        "type": "nodebalancer",
        "url": "/v4/nodebalancers/1234"
      }
    ],
    "id": 45678,
    "label": "very-cool-label",
    "rules": {
      "fingerprint": "abcdefg",
      "inbound": [],
      "inbound_policy": "DROP",
      "outbound": [],
      "outbound_policy": "DROP",
      "version": 1
    },
      "status": "enabled",
      "tags": [],
      "updated": "2020-04-10T13:34:01"
  }
]''']
