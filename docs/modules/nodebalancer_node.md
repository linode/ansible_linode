# nodebalancer_node

Manage Linode NodeBalancer Nodes.

- [Minimum Required Fields](#minimum-required-fields)
- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Minimum Required Fields
| Field       | Type  | Required     | Description                                                                                                                                                                                                              |
|-------------|-------|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `api_token` | `str` | **Required** | The Linode account personal access token. It is necessary to run the module. <br/>It can be exposed by the environment variable `LINODE_API_TOKEN` instead. <br/>See details in [Usage](https://github.com/linode/ansible_linode?tab=readme-ov-file#usage). |

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

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `nodebalancer_id` | <center>`int`</center> | <center>**Required**</center> | The ID of the NodeBalancer that contains this node.   |
| `config_id` | <center>`int`</center> | <center>**Required**</center> | The ID of the NodeBalancer Config that contains this node.   |
| `label` | <center>`str`</center> | <center>**Required**</center> | The label for this node. This is used to identify nodes within a config.   |
| `state` | <center>`str`</center> | <center>**Required**</center> | Whether the NodeBalancer node should be present or absent.  **(Choices: `present`, `absent`)** |
| `address` | <center>`str`</center> | <center>Optional</center> | The private IP Address where this backend can be reached. This must be a private IP address.  **(Updatable)** |
| `mode` | <center>`str`</center> | <center>Optional</center> | The mode this NodeBalancer should use when sending traffic to this backend.  **(Choices: `accept`, `reject`, `drain`, `backup`; Updatable)** |
| `weight` | <center>`int`</center> | <center>Optional</center> | Nodes with a higher weight will receive more traffic.  **(Updatable)** |

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
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-node-balancer-node) for a list of returned fields


