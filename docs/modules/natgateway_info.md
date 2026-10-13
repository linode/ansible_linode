# natgateway_info

Get info about a Linode NAT Gateway.

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
- name: Get info about a NAT Gateway by label
  linode.cloud.natgateway_info:
    label: my-nat-gateway
```

```yaml
- name: Get info about a NAT Gateway by ID
  linode.cloud.natgateway_info:
    id: 123
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>Optional</center> | The ID of the NAT Gateway to resolve.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the NAT Gateway to resolve.  **(Conflicts With: `id`)** |

## Return Values

- `natgateway` - The returned NAT Gateway.

    - Sample Response:
        ```json
        {
          "id": 123,
          "region": "us-east",
          "addresses": [
            { "address": "203.0.113.42" },
            { "address": "203.0.113.43" }
          ],
          "address_autoscale_max": 0,
          "default_ports_per_interface": 4096,
          "label": "my-ng",
          "portset_assignments": 0,
          "portset_capacity": 30,
          "vpc_subnet": {
            "id": 42,
            "type": "vpc_subnet",
            "label":"my-subnet",
            "url": "https://www.something.com/vpcs/42/subnets/41"
            "vpc_id": 13,
            "vpc_label": "my-vpc"
          },
          "created": "2026-01-01T00:01:01",
          "updated": "2026-03-01T00:01:01"
        }
        
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-natgateway) for a list of returned fields


