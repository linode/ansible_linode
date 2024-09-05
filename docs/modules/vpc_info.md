# vpc_info

Get info about a Linode VPC.

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
- name: Get info about a VPC by label
  linode.cloud.vpc_info:
    label: my-vpc
```

```yaml
- name: Get info about a VPC by ID
  linode.cloud.vpc_info:
    id: 12345
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the VPC to resolve.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the VPC to resolve.  **(Conflicts With: `id`)** |

## Return Values

- `vpc` - The returned VPC.

    - Sample Response:
        ```json
        {
            "created": "2023-08-31T18:35:01",
            "description": "A description of this VPC",
            "id": 344,
            "label": "my-vpc",
            "region": "us-east",
            "subnets": [],
            "updated": "2023-08-31T18:35:03"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-vpc) for a list of returned fields


