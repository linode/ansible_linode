# vpc

Create, read, and update a Linode VPC.

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
- name: Create a VPC 
  linode.cloud.vpc:
    label: my-vpc
    region: us-east
    description: A description of this VPC.
    state: present
```

```yaml
# NOTE: IPv6 VPCs may not currently be available to all users.
- name: Create a VPC with an auto-allocated IPv6 range
  linode.cloud.vpc:
    label: my-vpc
    region: us-east
    ipv6:
    - range: auto
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
| [`ipv6` (sub-options)](#ipv6) | <center>`list`</center> | <center>Optional</center> | A list of IPv6 ranges in CIDR notation. NOTE: IPv6 VPCs may currently be available to all users.   |

### ipv6

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `range` | <center>`str`</center> | <center>Optional</center> | The IPv6 range assigned to this VPC.   |
| `allocation_class` | <center>`str`</center> | <center>Optional</center> | The labeled IPv6 Inventory that the VPC Prefix should be allocated from.   |

## Return Values

- `vpc` - The VPC in JSON serialized form.

    - Sample Response:
        ```json
        {
            "created": "2023-08-31T18:35:01",
            "description": "A description of this VPC",
            "id": 344,
            "ipv6": [
                {
                    "range": "2001:db8:acad:0::/52"
                }
            ],
            "label": "my-vpc",
            "region": "us-east",
            "subnets": [],
            "updated": "2023-08-31T18:35:03"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-vpc) for a list of returned fields


