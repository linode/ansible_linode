# regions_vpc_availability_list

List and filter on Regions VPC Availability.

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
- name: List all of the Linode regions VPC availability
  linode.cloud.regions_vpc_availability_list:
    api_version: v4beta
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Regions VPC Availability in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Regions VPC Availability by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Regions VPC Availability.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Regions VPC Availability to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-regions-vpc-availability).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `regions_vpc_availability` - The returned Regions VPC Availability.

    - Sample Response:
        ```json
        [
            {
                "region": "nl-ams",
                "available": true,
                "available_ipv6_prefix_lengths": [
                    48,
                    52
                ]
            },
            {
                "region": "fr-par-2",
                "available": true,
                "available_ipv6_prefix_lengths": [
                    48,
                    52
                ]
            },
            {
                "region": "jp-tyo-3",
                "available": true,
                "available_ipv6_prefix_lengths": [
                    48,
                    52
                ]
            }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-regions-vpc-availability) for a list of returned fields


