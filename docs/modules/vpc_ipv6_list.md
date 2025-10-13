# vpc_ipv6_list

List and filter on all VPC IPv6 addresses for a given VPC.

NOTE: IPv6 VPCs may not currently be available to all users.

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
- name: List all IPv6 addresses for a specific VPC.
  linode.cloud.vpc_ipv6_list:
    vpc_id: 12345
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `vpc_id` | <center>`int`</center> | <center>**Required**</center> | The parent VPC for the VPC IPv6 Addresses.   |
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list VPC IPv6 Addresses in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order VPC IPv6 Addresses by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting VPC IPv6 Addresses.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of VPC IPv6 Addresses to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-vpc-ipv6s).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `addresses` - The returned VPC IPv6 Addresses.

    - Sample Response:
        ```json
        [
          {
            "active": false,
            "address": null,
            "address_range": null,
            "config_id": 123,
            "database_id": null,
            "gateway": null,
            "interface_id": 123,
            "ipv6_addresses": [
              {
                "slaac_address": "2001:db8:acad:1:abcd:ef12:3456:7890"
              }
            ],
            "ipv6_is_public": false,
            "ipv6_range": "2001:db8:acad:1::/64",
            "linode_id": 123,
            "nat_1_1": "",
            "nodebalancer_id": null,
            "prefix": 64,
            "region": "us-mia",
            "subnet_id": 123,
            "subnet_mask": "",
            "vpc_id": 123
          },
          {
            "active": false,
            "address": null,
            "address_range": null,
            "config_id": 123,
            "database_id": null,
            "gateway": null,
            "interface_id": 123,
            "ipv6_addresses": [],
            "ipv6_is_public": false,
            "ipv6_range": "2001:db8::/64",
            "linode_id": 123,
            "nat_1_1": "",
            "nodebalancer_id": null,
            "prefix": 64,
            "region": "us-mia",
            "subnet_id": 271170,
            "subnet_mask": "",
            "vpc_id": 262108
          },
          {
            "active": false,
            "address": null,
            "address_range": null,
            "config_id": 123,
            "database_id": null,
            "gateway": null,
            "interface_id": 123,
            "ipv6_addresses": [],
            "ipv6_is_public": false,
            "ipv6_range": "2001:db8::/64",
            "linode_id": 123,
            "nat_1_1": "",
            "nodebalancer_id": null,
            "prefix": 64,
            "region": "us-mia",
            "subnet_id": 123,
            "subnet_mask": "",
            "vpc_id": 123
          }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-vpc-ipv6s) for a list of returned fields


