# vpc_subnet_info

Get info about a Linode VPC Subnet.

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
- name: Get info about a VPC Subnet by label
  linode.cloud.vpc_subnet_info:
    vpc_id: 12345
    label: my-subnet
```

```yaml
- name: Get info about a VPC Subnet by ID
  linode.cloud.vpc_subnet_info:
    vpc_id: 12345
    id: 123
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `vpc_id` | <center>`int`</center> | <center>**Required**</center> | The ID of the VPC for this resource.   |
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the VPC Subnet to resolve.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the VPC Subnet to resolve.  **(Conflicts With: `id`)** |

## Return Values

- `subnet` - The returned VPC Subnet.

    - Sample Response:
        ```json
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
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-vpc-subnet) for a list of returned fields


