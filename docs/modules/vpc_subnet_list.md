# vpc_subnet_list

List and filter on VPC Subnets.

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
- name: List all of the subnets under a VPC
  linode.cloud.vpc_subnet_list:
    vpc_id: 12345
  
```

```yaml
- name: List all of the subnets with a given label under a VPC
  linode.cloud.vpc_subnet_list:
    vpc_id: 12345
    filters:
      - name: label
        values: my-subnet
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `vpc_id` | <center>`int`</center> | <center>**Required**</center> | The parent VPC for the VPC Subnets.   |
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list VPC Subnets in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order VPC Subnets by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting VPC Subnets.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of VPC Subnets to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-vpc-subnets).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `subnets` - The returned VPC Subnets.

    - Sample Response:
        ```json
        [
            {
                "created": "2023-08-31T18:53:04",
                "id": 271,
                "ipv4": "10.0.0.0/24",
                "label": "test-subnet",
                "linodes": [
                    {
                        "id": 1234567,
                        "interfaces": [{"active": false, "id": 654321}]
                    }
                ],
                "updated": "2023-08-31T18:53:04"
            }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-vpc-subnets) for a list of returned fields


