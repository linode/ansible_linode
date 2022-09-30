# nodebalancer

Manage a Linode NodeBalancer.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

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
| `label` | `str` | **Required** | The unique label to give this NodeBalancer.   |
| `state` | `str` | **Required** | The desired state of the target.  (Choices:  `present`  `absent` ) |
| `client_conn_throttle` | `int` | Optional | Throttle connections per second. Set to 0 (zero) to disable throttling.   |
| `region` | `str` | Optional | The ID of the Region to create this NodeBalancer in.   |
| [`configs` (sub-options)](#configs) | `list` | Optional | A list of configs to apply to the NodeBalancer.   |





### configs

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `algorithm` | `str` | Optional | What algorithm this NodeBalancer should use for routing traffic to backends.  (Choices:  `roundrobin`  `leastconn`  `source` ) |
| `check` | `str` | Optional | The type of check to perform against backends to ensure they are serving requests.  (Choices:  `none`  `connection`  `http`  `http_body` ) |
| `check_attempts` | `int` | Optional | How many times to attempt a check before considering a backend to be down.   |
| `check_body` | `str` | Optional | This value must be present in the response body of the check in order for it to pass. If this value is not present in the response body of a check request, the backend is considered to be down.   |
| `check_interval` | `int` | Optional | How often, in seconds, to check that backends are up and serving requests.   |
| `check_passive` | `bool` | Optional | If true, any response from this backend with a 5xx status code will be enough for it to be considered unhealthy and taken out of rotation.   |
| `check_path` | `str` | Optional | The URL path to check on each backend. If the backend does not respond to this request it is considered to be down.   |
| `check_timeout` | `int` | Optional | How long, in seconds, to wait for a check attempt before considering it failed.   |
| `cipher_suite` | `str` | Optional | What ciphers to use for SSL connections served by this NodeBalancer.  (Choices:  `recommended`  `legacy` Default: `recommended`) |
| `port` | `int` | Optional | The port this Config is for.   |
| `protocol` | `str` | Optional | The protocol this port is configured to serve.  (Choices:  `http`  `https`  `tcp` ) |
| `proxy_protocol` | `str` | Optional | ProxyProtocol is a TCP extension that sends initial TCP connection information such as source/destination IPs and ports to backend devices.  (Choices:  `none`  `v1`  `v2` ) |
| `recreate` | `bool` | Optional | If true, the config will be forcibly recreated on every run. This is useful for updates to redacted fields (`ssl_cert`, `ssl_key`)  (Default: `False`) |
| `ssl_cert` | `str` | Optional | The PEM-formatted public SSL certificate (or the combined PEM-formatted SSL certificate and Certificate Authority chain) that should be served on this NodeBalancerConfig’s port.   |
| `ssl_key` | `str` | Optional | The PEM-formatted private key for the SSL certificate set in the ssl_cert field.   |
| `stickiness` | `str` | Optional | Controls how session stickiness is handled on this port.  (Choices:  `none`  `table`  `http_cookie` ) |
| [`nodes` (sub-options)](#nodes) | `list` | Optional | A list of nodes to apply to this config. These can alternatively be configured through the nodebalancer_node module.   |





### nodes

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | `str` | **Required** | The label for this node.   |
| `address` | `str` | **Required** | The private IP Address where this backend can be reached. This must be a private IP address.   |
| `weight` | `int` | Optional | Nodes with a higher weight will receive more traffic.   |
| `mode` | `str` | Optional | The mode this NodeBalancer should use when sending traffic to this backend.  (Choices:  `accept`  `reject`  `drain`  `backup` ) |






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
    - See the [Linode API response documentation](https://www.linode.com/docs/api/nodebalancers/#nodebalancer-view__responses) for a list of returned fields


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
    - See the [Linode API response documentation](https://www.linode.com/docs/api/nodebalancers/#config-view__responses) for a list of returned fields


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
    - See the [Linode API response documentation](https://www.linode.com/docs/api/nodebalancers/#node-view) for a list of returned fields


