# ip

Allocates a new IPv4 Address on your Account, or updates an existing one. 

To allocate, the Linode must be configured to support 

additional addresses - 

please open a support ticket 

requesting additional addresses before attempting allocation.

To allocate a new reserved IP, provide region, type, and set reserved=true.

To promote an existing IP to reserved, provide the address and set reserved=true.

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
- name: Allocate IP to Linode
  linode.cloud.ip:
    linode_id: 123
    public: true
    type: ipv4
    state: present
```

```yaml
- name: Promote an existing IP to reserved
  linode.cloud.ip:
    address: "97.107.143.141"
    reserved: true
    state: present
```

```yaml
- name: Allocate a new reserved IP in a region
  linode.cloud.ip:
    region: us-east
    type: ipv4
    reserved: true
    state: present
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `state` | <center>`str`</center> | <center>**Required**</center> | The state of this IP.  **(Choices: `present`, `absent`)** |
| `linode_id` | <center>`int`</center> | <center>Optional</center> | The ID of a Linode you have access to  that this address will be allocated to.   |
| `public` | <center>`bool`</center> | <center>Optional</center> | Whether to create a public or private IPv4 address.   |
| `type` | <center>`str`</center> | <center>Optional</center> | The type of address you are requesting.  Only IPv4 addresses may be allocated through this operation.  **(Choices: `ipv4`)** |
| `address` | <center>`str`</center> | <center>Optional</center> | The IP address to update or delete. Required when updating an existing IP (e.g., promoting to reserved)  or when deleting (state=absent).  **(Conflicts With: `linode_id`,`public`,`type`)** |
| `reserved` | <center>`bool`</center> | <center>Optional</center> | Whether this IP address should be reserved. Setting to true promotes an existing allocated IP to a reserved IP  via PUT /networking/ips/{address}. Requires the address parameter.   |
| `tags` | <center>`list`</center> | <center>Optional</center> | Tags to apply to this IP address. NOTE: Tags are replaced entirely on update, not appended. Only applicable when updating an existing IP via the address parameter.  **(Updatable)** |
| `region` | <center>`str`</center> | <center>Optional</center> | The region in which to allocate a new reserved IP address. Required when allocating a new reserved IP (reserved=true) without  specifying an existing address.  **(Conflicts With: `linode_id`,`public`,`address`)** |

## Return Values

- `ip` - The IP address in JSON serialized form.

    - Sample Response:
        ```json
        {
          "address": "97.107.143.141",
          "assigned_entity": null,
          "gateway": "97.107.143.1",
          "interface_id": null,
          "linode_id": 123,
          "prefix": 24,
          "public": true,
          "rdns": "test.example.org",
          "region": "us-east",
          "reserved": false,
          "subnet_mask": "255.255.255.0",
          "tags": [],
          "type": "ipv4",
          "vpc_nat_1_1": {
            "vpc_id": 242,
            "subnet_id": 194,
            "address": "139.144.244.36"
          }
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-ip) for a list of returned fields


