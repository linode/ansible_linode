# vpc

Create, read, and update a Linode VPC.

LINODE_API_TOKEN environment variable is required.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create a VPC 
  linode.cloud.vpc:
    label: my-vpc
    region: us-east
    description: A description of this VPC.
    state: present
```

```yaml
- name: Delete a VPC
  linode.cloud.vpc:
    label: my-vpc
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | <center>`str`</center> | <center>**Required**</center> | This VPC's unique label.   |
| `state` | <center>`str`</center> | <center>**Required**</center> | The state of this token.  **(Choices: `present`, `absent`)** |
| `description` | <center>`str`</center> | <center>Optional</center> | A description describing this VPC.   |
| `region` | <center>`str`</center> | <center>Optional</center> | The region this VPC is located in.   |

## Return Values

- `vpc` - The VPC in JSON serialized form.

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
    - See the [Linode API response documentation](TODO) for a list of returned fields


