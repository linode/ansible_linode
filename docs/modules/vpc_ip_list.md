# vpc_ip_list

List and filter on VPC IP Addresses.

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
- name: List all IPs of a specific VPC.
  linode.cloud.vpc_ip_list:
    vpc_id: 12345
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `vpc_id` | <center>`int`</center> | <center>**Required**</center> | The parent VPC for the VPC IP Addresses.   |
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list VPC IP Addresses in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order VPC IP Addresses by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting VPC IP Addresses.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of VPC IP Addresses to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-vpc-ips).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `vpcs_ips` - The returned VPC IP Addresses.

    - Sample Response:
        ```json
        [
            {
                "address": "10.0.0.2",
                "address_range": null,
                "vpc_id": 56242,
                "subnet_id": 55829,
                "region": "us-mia",
                "linode_id": 57328104,
                "config_id": 60480976,
                "interface_id": 1373818,
                "active": false,
                "nat_1_1": null,
                "gateway": "10.0.0.1",
                "prefix": 24,
                "subnet_mask": "255.255.255.0"
            }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-vpc-ips) for a list of returned fields


