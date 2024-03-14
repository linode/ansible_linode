# vpc_info

Get info about a Linode VPC.

LINODE_API_TOKEN environment variable is required.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

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
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the VPC to resolve.  **(Conflicts With: `id`)** |
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the VPC to resolve.  **(Conflicts With: `label`)** |

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


