# region_list

List and filter on Linode Regions.

LINODE_API_TOKEN environment variable is required.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: List all of the Linode regions
  linode.cloud.region_list: {}
```

```yaml
- name: Resolve all Linode regions
  linode.cloud.region_list:
    filters:
      - name: id
        values: us-east
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list regions in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order regions by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting regions.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of results to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable attributes can be found here: https://www.linode.com/docs/api/regions/#regions-list__responses   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `regions` - The returned regions.

    - Sample Response:
        ```json
        [
           {
              "capabilities": [
                "Linodes",
                "NodeBalancers",
                "Block Storage",
                "Object Storage"
              ],
              "country": "us",
              "id": "us-east",
              "label": "Newark, NJ, USA",
              "resolvers": {
                "ipv4": "192.0.2.0,192.0.2.1",
                "ipv6": "2001:0db8::,2001:0db8::1"
              },
              "status": "ok"
            }
        ]
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/regions/#regions-list__response-samples) for a list of returned fields


