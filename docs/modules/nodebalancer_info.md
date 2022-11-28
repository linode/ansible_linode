# nodebalancer_info

Get info about a Linode NodeBalancer.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Get a NodeBalancer by its id
  linode.cloud.nodebalancer_info:
    id: 12345
```

```yaml
- name: Get a NodeBalancer by its label
  linode.cloud.nodebalancer_info:
    label: cool_nodebalancer
```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of this NodeBalancer. Optional if `label` is defined.   |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of this NodeBalancer. Optional if `id` is defined.   |






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


