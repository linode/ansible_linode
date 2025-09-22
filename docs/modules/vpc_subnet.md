# vpc_subnet

Create, read, and update a Linode VPC Subnet.

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
- name: Create a VPC subnet
  linode.cloud.vpc_subnet:
    vpc_id: 12345
    label: my-subnet
    ipv4: '10.0.0.0/24'
    state: present
```

```yaml
# NOTE: IPv6 VPCs may not currently be available to all users.
- name: Create a VPC subnet with an auto-allocated IPv6 range
  linode.cloud.vpc_subnet:
    vpc_id: 12345
    label: my-subnet
    ipv6:
    - range: auto
    state: present
```

```yaml'
- name: Delete a VPC Subnet
  linode.cloud.vpc_subnet:
    vpc_id: 12345
    label: my-subnet
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `vpc_id` | <center>`int`</center> | <center>**Required**</center> | The ID of the parent VPC for this subnet.   |
| `label` | <center>`str`</center> | <center>**Required**</center> | This VPC's unique label.   |
| `state` | <center>`str`</center> | <center>**Required**</center> | The state of this token.  **(Choices: `present`, `absent`)** |
| `ipv4` | <center>`str`</center> | <center>Optional</center> | The IPV4 range for this subnet in CIDR format.   |
| [`ipv6` (sub-options)](#ipv6) | <center>`list`</center> | <center>Optional</center> | The IPv6 ranges of this subnet. NOTE: IPv6 VPCs may currently be available to all users.   |

### ipv6

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `range` | <center>`str`</center> | <center>Optional</center> | An existing IPv6 prefix owned by the current account or a forward slash (/) followed by a valid prefix length. If unspecified, a range with the default prefix will be allocated for this VPC.   |

## Return Values

- `subnet` - The VPC in JSON serialized form.

    - Sample Response:
        ```json
        {
            "created": "2023-08-31T18:53:04",
            "id": 271,
            "ipv4": "10.0.0.0/24",
            "ipv6": [
                {
                    "range": "2001:db8:acad:300::/56"
                }
            ],
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


