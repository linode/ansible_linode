# vpc_default_ranges_info

Get info about a Linode VPC Default Ranges.

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
- name: Get info about the default and forbidden IPv4 address ranges for VPCs
  linode.cloud.vpc_default_ranges_info:

```


## Return Values

- `vpc_default_ranges` - The returned VPC Default Ranges.

    - Sample Response:
        ```json
        
        {
          "default_ipv4_ranges": [
            "10.0.0.0/8",
            "172.16.0.0/12",
            "192.168.0.0/17"
          ],
          "forbidden_ipv4_ranges": [
            "0.0.0.0/8",
            "10.64.12.199/24",
            "172.21.89.19/15",
            "192.168.128.0/17",
            "203.0.113.190/32"
          ]
        }
        
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-vpcs-default-ranges) for a list of returned fields


