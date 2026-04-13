# region_vpc_availability_info

Get info about a Linode Region VPC Availability.

WARNING! This module makes use of beta endpoints and requires the C(api_version) field be explicitly set to C(v4beta).

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
- name: Get Info of a Linode Region VPC Availability
  linode.cloud.region_vpc_availability_info:
    id: us-mia
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>**Required**</center> | The ID of the Region VPC Availability to resolve.   |

## Return Values

- `region_vpc_availability` - The returned Region VPC Availability.

    - Sample Response:
        ```json
        {
            "region": "us-mia",
            "available": true,
            "available_ipv6_prefix_lengths": [
                48,
                52
            ]
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-region-vpc-availability) for a list of returned fields


