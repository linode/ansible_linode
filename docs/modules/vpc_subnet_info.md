# vpc_subnet_info

Get info about a Linode VPC Subnet.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

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
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the VPC Subnet to resolve.   |
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the VPC Subnet to resolve.   |

## Return Values

- `subnet` - The returned VPC Subnet.

    - Sample Response:
        ```json
        {
            "created": "2023-08-31T18:53:04",
            "id": 271,
            "ipv4": "10.0.0.0/24",
            "label": "test-subnet",
            "linodes": [],
            "updated": "2023-08-31T18:53:04"
        }
        ```


