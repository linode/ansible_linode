# nodebalancer_vpc_info

Get info about a Linode VPC Configuration.

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
- name: Get a NodeBalancer VPC configuration by its id
  linode.cloud.nodebalancer_vpc_info:
    id: 12345
    vpc_config_id: 123
```

```yaml
- name: Get a NodeBalancer by its label
  linode.cloud.nodebalancer_vpc_info:
    label: cool_nodebalancer
    vpc_config_id: 123
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `vpc_config_id` | <center>`int`</center> | <center>**Required**</center> | The ID of the VPC Config for this resource.   |
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the NodeBalancer to retrieve the VPC configuration from.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the NodeBalancer to retrieve the VPC configuration from.  **(Conflicts With: `id`)** |

## Return Values

- `vpc_config` - The returned VPC Configuration.

    - Sample Response:
        ```json
        
          {
            "id": 123,
            "nodebalancer_id": 12345,
            "subnet_id": 456,
            "vpc_id": 789,
            "ipv4_range": "10.0.0.4/30",
            "ipv6_range": null,
            "purpose": "backend"
          }
        
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-node-balancer-vpc-config) for a list of returned fields


