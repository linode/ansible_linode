# vpc_list

List and filter on VPCs.

LINODE_API_TOKEN environment variable is required.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: List all of the VPCs for the current user
  linode.cloud.vpc_list: {}
```

```yaml
- name: List all of the VPCS for the current user with the given label
  linode.cloud.vpc_list:
    filters:
      - name: label
        values: my-vpc
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list VPCs in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order VPCs by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting VPCs.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of VPCs to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here]().   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `vpcs` - The returned VPCs.

    - Sample Response:
        ```json
        [
            {
                "created": "2023-08-31T18:35:01",
                "description": "A description of this VPC",
                "id": 344,
                "label": "my-vpc",
                "region": "us-east",
                "subnets": [],
                "updated": "2023-08-31T18:35:03"
            }
        ]
        ```


