# nodebalancer

Manage a Linode NodeBalancer.

NOTE: UDP NodeBalancer may not currently be available to all users.

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
            address: 0.0.0.0:80
```

```yaml
- name: Delete the NodeBalancer
  linode.cloud.nodebalancer:
    label: my-loadbalancer
    region: us-east
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | <center>`str`</center> | <center>**Required**</center> | The unique label to give this NodeBalancer.   |
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the target.  **(Choices: `present`, `absent`)** |
| `client_conn_throttle` | <center>`int`</center> | <center>Optional</center> | Throttle connections per second. Set to 0 (zero) to disable throttling.  **(Updatable)** |
| `client_udp_sess_throttle` | <center>`int`</center> | <center>Optional</center> | Throttle UDP sessions per second (0-20). Set to 0 (zero) to disable throttling.  **(Updatable)** |
| `region` | <center>`str`</center> | <center>Optional</center> | The ID of the Region to create this NodeBalancer in.   |
| `firewall_id` | <center>`int`</center> | <center>Optional</center> | The ID of the Firewall to assign this NodeBalancer to.   |
| `tags` | <center>`list`</center> | <center>Optional</center> | Tags to assign to this NodeBalancer.  **(Updatable)** |
| [`configs` (sub-options)](#configs) | <center>`list`</center> | <center>Optional</center> | A list of configs to apply to the NodeBalancer.  **(Updatable)** |

### configs

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `algorithm` | <center>`str`</center> | <center>Optional</center> | What algorithm this NodeBalancer should use for routing traffic to backends.  **(Choices: `roundrobin`, `leastconn`, `source`, `ring_hash`; Updatable)** |
| `check` | <center>`str`</center> | <center>Optional</center> | The type of check to perform against backends to ensure they are serving requests.  **(Choices: `none`, `connection`, `http`, `http_body`; Updatable)** |
| `check_attempts` | <center>`int`</center> | <center>Optional</center> | How many times to attempt a check before considering a backend to be down.  **(Updatable)** |
| `check_body` | <center>`str`</center> | <center>Optional</center> | This value must be present in the response body of the check in order for it to pass. If this value is not present in the response body of a check request, the backend is considered to be down.  **(Updatable)** |
| `check_interval` | <center>`int`</center> | <center>Optional</center> | How often, in seconds, to check that backends are up and serving requests.  **(Updatable)** |
| `check_passive` | <center>`bool`</center> | <center>Optional</center> | If true, any response from this backend with a 5xx status code will be enough for it to be considered unhealthy and taken out of rotation.  **(Updatable)** |
| `check_path` | <center>`str`</center> | <center>Optional</center> | The URL path to check on each backend. If the backend does not respond to this request it is considered to be down.  **(Updatable)** |
| `check_timeout` | <center>`int`</center> | <center>Optional</center> | How long, in seconds, to wait for a check attempt before considering it failed.  **(Updatable)** |
| `udp_check_port` | <center>`int`</center> | <center>Optional</center> | Specifies the port on the backend node used for active health checks, which may differ from the port serving traffic.  **(Updatable)** |
| `cipher_suite` | <center>`str`</center> | <center>Optional</center> | What ciphers to use for SSL connections served by this NodeBalancer.  **(Choices: `recommended`, `legacy`, `none`; Updatable)** |
| `port` | <center>`int`</center> | <center>Optional</center> | The port this Config is for.  **(Updatable)** |
| `protocol` | <center>`str`</center> | <center>Optional</center> | The protocol this port is configured to serve.  **(Choices: `http`, `https`, `tcp`, `udp`; Updatable)** |
| `proxy_protocol` | <center>`str`</center> | <center>Optional</center> | ProxyProtocol is a TCP extension that sends initial TCP connection information such as source/destination IPs and ports to backend devices.  **(Choices: `none`, `v1`, `v2`; Updatable)** |
| `recreate` | <center>`bool`</center> | <center>Optional</center> | If true, the config will be forcibly recreated on every run. This is useful for updates to redacted fields (`ssl_cert`, `ssl_key`)  **(Default: `False`)** |
| `ssl_cert` | <center>`str`</center> | <center>Optional</center> | The PEM-formatted public SSL certificate (or the combined PEM-formatted SSL certificate and Certificate Authority chain) that should be served on this NodeBalancerConfig’s port.  **(Updatable)** |
| `ssl_key` | <center>`str`</center> | <center>Optional</center> | The PEM-formatted private key for the SSL certificate set in the ssl_cert field.  **(Updatable)** |
| `stickiness` | <center>`str`</center> | <center>Optional</center> | Controls how session stickiness is handled on this port.  **(Choices: `none`, `table`, `http_cookie`, `session`, `source_ip`; Updatable)** |
| [`nodes` (sub-options)](#nodes) | <center>`list`</center> | <center>Optional</center> | A list of nodes to apply to this config. These can alternatively be configured through the nodebalancer_node module.  **(Updatable)** |

### nodes

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | <center>`str`</center> | <center>**Required**</center> | The label for this node.   |
| `address` | <center>`str`</center> | <center>**Required**</center> | The private IP Address where this backend can be reached. This must be a private IP address.  **(Updatable)** |
| `weight` | <center>`int`</center> | <center>Optional</center> | Nodes with a higher weight will receive more traffic.  **(Updatable)** |
| `mode` | <center>`str`</center> | <center>Optional</center> | The mode this NodeBalancer should use when sending traffic to this backend.  **(Choices: `accept`, `reject`, `drain`, `backup`; Updatable)** |

## Return Values

- `node_balancer` - The NodeBalancer in JSON serialized form.

    - Sample Response:
        ```json
        {
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
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-node-balancer) for a list of returned fields


- `configs` - A list of configs applied to the NodeBalancer.

    - Sample Response:
        ```json
        [
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
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-node-balancer-config) for a list of returned fields


- `nodes` - A list of configs applied to the NodeBalancer.

    - Sample Response:
        ```json
        [
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
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-node-balancer-node) for a list of returned fields


- `firewalls` - A list IDs for firewalls attached to this NodeBalancer.

    - Sample Response:
        ```json
        [
          1234,
          5678
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-node-balancer-firewalls) for a list of returned fields


