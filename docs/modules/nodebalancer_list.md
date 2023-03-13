# nodebalancer_list

List and filter on Nodebalancers.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: List all of the Nodebalancers for the current Linode Account
  linode.cloud.nodebalancer_list: {}
```

```yaml
- name: Resolve all Nodebalancers for the current Linode Account
  linode.cloud.nodebalancer_list:
    filter:
      - name: label
        values: myNodebalancerLabel
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list nodebalancers in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order nodebalancers by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting nodebalancers.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of results to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable attributes can be found here: https://www.linode.com/docs/api/nodebalancers/#nodebalancers-list__responses   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `nodebalancers` - The returned nodebalancers.

    - Sample Response:
        ```json
        [
            {
              "client_conn_throttle": 0,
              "created": "2018-01-01T00:01:01",
              "hostname": "192.0.2.1.ip.linodeusercontent.com",
              "id": 12345,
              "ipv4": "203.0.113.1",
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
        ]
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/nodebalancers/#nodebalancers-list__response-samples) for a list of returned fields


