# nodebalancer_info

Get info about a Linode Node Balancer.

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
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the Node Balancer to resolve.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the Node Balancer to resolve.  **(Conflicts With: `id`)** |

## Return Values

- `node_balancer` - The returned Node Balancer.

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


- `configs` - The returned configs.

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
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-node-balancer-configs) for a list of returned fields


- `nodes` - The returned nodes.

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
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-node-balancer-config-nodes) for a list of returned fields


- `firewalls` - The returned firewalls.

    - Sample Response:
        ```json
        [
          1234,
          5678
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-node-balancer-firewalls) for a list of returned fields


- `firewalls_data` - The returned firewalls_data.

    - Sample Response:
        ```json
        [
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
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-node-balancer-firewalls) for a list of returned fields


