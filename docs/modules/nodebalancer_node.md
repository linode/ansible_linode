# nodebalancer_node

Manage Linode NodeBalancer Nodes.


## Examples

```yaml
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

    state: present
```


## Parameters


- `nodebalancer_id` - **(Required)** The ID of the NodeBalancer that contains this node. 
- `config_id` - **(Required)** The ID of the NodeBalancer Config that contains this node. 
- `label` - **(Required)** The label for this node. This is used to identify nodes within a config. 
- `address` -  The private IP Address where this backend can be reached. This must be a private IP address. 
- `state` - **(Required)** Whether the NodeBalancer node should be present or absent. 
- `mode` -  The mode this NodeBalancer should use when sending traffic to this backend. 
- `weight` -  Nodes with a higher weight will receive more traffic. 


## Return Values

- `node` - The NodeBalancer Node in JSON serialized form.

    - Sample Response:
        ```json
        {
          "address": "123.123.123.123:80",
          "config_id": 12345,
          "id": 12345,
          "label": "mynode",
          "mode": "accept",
          "nodebalancer_id": 12345,
          "status": "Unknown",
          "weight": 10
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/nodebalancers/#node-view__responses) for a list of returned fields


