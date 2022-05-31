"""Documentation fragments for the nodebalancer_node module"""

specdoc_examples = ['''
- name: Create a NodeBalancer
  linode.cloud.nodebalancer:
    label: my-nodebalancer
    region: us-east
    state: present
    configs:
      - port: 80
        protocol: http
        algorithm: roundrobin
  register: nodebalancer_result

- name: Create an Instance
  linode.cloud.instance:
    label: my-instance
    region: us-east
    private_ip: true
    type: g6-standard-1
    state: present
  register: instance_result

- name: Attach the Instance to the NodeBalancer
  linode.cloud.nodebalancer_node:
    nodebalancer_id: nodebalancer_result.node_balancer.id
    config_id: nodebalancer_result.configs[0].id

    label: my-node

    # Use the private ip address of the instance
    address: '{{ instance_result.instance.ipv4[1] }}:80'

    state: present''']

result_node_samples = ['''{
  "address": "123.123.123.123:80",
  "config_id": 12345,
  "id": 12345,
  "label": "mynode",
  "mode": "accept",
  "nodebalancer_id": 12345,
  "status": "Unknown",
  "weight": 10
}''']
