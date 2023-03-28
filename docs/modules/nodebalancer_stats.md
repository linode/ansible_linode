# nodebalancer_stats

View a Linode NodeBalancers Stats.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: List all of the Nodebalancer Stats for the Nodebalancer with the given id
  linode.cloud.nodebalancer_stats:
    id: 12345
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>Optional</center> | The id of the nodebalancer for which the statistics apply to.   |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the nodebalancer for which the statistics apply to.   |

## Return Values

- `node_balancer_stats` - The NodeBalancer Stats in JSON serialized form.

    - Sample Response:
        ```json
        [
           {
              "connections": [
                null
               ],
               "traffic": {
                "in": [
                    null
                ],
                "out": [
                    null
                ]
               }
               "title" : "sample-title"
            }
        ]
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/nodebalancers/#nodebalancer-statistics-view__responses) for a list of returned fields


