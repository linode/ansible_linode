# region_vpc_availability_info

Get info about a Linode Region VPC Availability.

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
- name: Get info about VPC availability for a region
  linode.cloud.region_vpc_availability_info:
    region: us-east

```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `region` | <center>`str`</center> | <center>**Required**</center> | The Region of the Region VPC Availability to resolve.   |

## Return Values

- `vpc_availability` - The returned Region VPC Availability.

    - Sample Response:
        ```json
        
        {
          "region": "us-east",
          "available": true,
          "available_ipv6_prefix_lengths": [52]
        }
        
        ```
    - See the [Linode API response documentation](TODO) for a list of returned fields


