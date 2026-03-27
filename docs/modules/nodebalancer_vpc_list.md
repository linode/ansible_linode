# nodebalancer_vpc_list

List and filter on Node Balancer VPC Configurations.

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
- name: List all of the Nodebalancer VPC configurations for a specific NodeBalancer
  linode.cloud.nodebalancer_vpc_list:
    nodebalancer_id: 123
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `nodebalancer_id` | <center>`int`</center> | <center>**Required**</center> | The parent NodeBalancer for the Node Balancer VPC Configurations.   |
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Node Balancer VPC Configurations in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Node Balancer VPC Configurations by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Node Balancer VPC Configurations.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Node Balancer VPC Configurations to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-node-balancer-vpcs).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `nodebalancer_vpc_configs` - The returned Node Balancer VPC Configurations.

    - Sample Response:
        ```json
        [
          {
              "id": 123,
              "nodebalancer_id": 456,
              "vpc_id": 89,
              "subnet_id": 21,
              "ipv4_range": "10.0.0.3/32",
              "ipv6_range": null,
              "purpose": "frontend"
          },
          {
              "id": 124,
              "nodebalancer_id": 457,
              "vpc_id": 90,
              "subnet_id": 22,
              "ipv4_range": "10.0.0.4/30",
              "ipv6_range": "/64",
              "purpose": "backend"
          }
        ],
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-node-balancer-vpcs) for a list of returned fields


