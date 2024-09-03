# nodebalancer_stats

Get info about a Linode Node Balancer Stats.

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
- name: List all of the Nodebalancer Stats for the Nodebalancer with the given id
  linode.cloud.nodebalancer_stats:
    id: 12345
- name: List all of the Nodebalancer Stats for the Nodebalancer with the given label
  linode.cloud.nodebalancer_stats:
    label: example_label
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the Node Balancer Stats to resolve.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the Node Balancer Stats to resolve.  **(Conflicts With: `id`)** |

## Return Values

- `node_balancer_stats` - The returned Node Balancer Stats.

    - Sample Response:
        ```json
        [
          {
            "connections": [
              1679586600000,
              0
            ],
            "traffic": {
              "in": [
                1679586600000,
                0
              ],
              "out": [
                1679586600000,
                0
              ]
            },
            "title" : "sample-title"
          }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-node-balancer-stats) for a list of returned fields


