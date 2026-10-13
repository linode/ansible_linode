# natgateway

Manage a NAT Gateway.

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
- name: Create a natgateway
  linode.cloud.natgateway:
    label: my-ng
    region: us-east
    addresses:
        - address: 203.0.113.42
        - address: 203.0.113.43
    default_ports_per_interface: 4096
    use_autoscaling: false
    vpc_subnet_id: 42
    state: present
```

```yaml
- name: Update a NAT Gateway label
  linode.cloud.natgateway:
    id: 123
    label: my-ng-updated
    state: present
```

```yaml
- name: Delete a NAT Gateway by label
  linode.cloud.natgateway:
    label: my-ng
    state: absent
```

```yaml
- name: Delete a NAT Gateway by id
  linode.cloud.natgateway:
    id: 123
    state: absent

```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the target.  **(Choices: `present`, `absent`)** |
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the NAT Gateway.   |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the NAT Gateway. This field can only contain ASCII letters, digits and dashes.  **(Updatable)** |
| [`addresses` (sub-options)](#addresses) | <center>`list`</center> | <center>Optional</center> | The list of IP addresses assigned to the NAT Gateway.  **(Updatable)** |
| `region` | <center>`str`</center> | <center>Optional</center> | The region that the NAT Gateway is in.   |
| `default_ports_per_interface` | <center>`int`</center> | <center>Optional</center> | The default number of ports per interface.   |
| `use_autoscaling` | <center>`bool`</center> | <center>Optional</center> | Whether or not to use autoscaling.   |
| `vpc_subnet_id` | <center>`int`</center> | <center>Optional</center> | The ID of the VPC subnet that the NAT Gateway is in.   |

### addresses

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `address` | <center>`str`</center> | <center>Optional</center> | The IPv4 address.   |

## Return Values

- `natgateway` - The returned NAT Gateway.

    - Sample Response:
        ```json
        {
          "id": 123,
          "region": "us-east",
          "addresses": [
            { "address": "203.0.113.42" },
            { "address": "203.0.113.43" }
          ],
          "address_autoscale_max": 0,
          "default_ports_per_interface": 4096,
          "label": "my-ng",
          "portset_assignments": 0,
          "portset_capacity": 30,
          "vpc_subnet": {
            "id": 42,
            "type": "vpc_subnet",
            "label":"my-subnet",
            "url": "https://www.something.com/vpcs/42/subnets/41"
            "vpc_id": 13,
            "vpc_label": "my-vpc"
          },
          "created": "2026-01-01T00:01:01",
          "updated": "2026-03-01T00:01:01"
        }
        
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-natgateway) for a list of returned fields


- `addresses` - The list of IP addresses assigned to the NAT Gateway.

    - Sample Response:
        ```json
        [
          {
              "address": "203.0.113.43",
              "in_use": true,
              "interface_count": 6,
              "portset_assignments": 6,
              "portset_capacity": 63
            },
            {
              "address": "203.0.113.44",
              "in_use": false,
              "interface_count": 0,
              "portset_assignments": 0,
              "portset_capacity": 63
          }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-natgateway-addresses) for a list of returned fields


