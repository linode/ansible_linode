# ip

Allocates a new IPv4 Address on your Account. The Linode must be configured to support additional addresses - please Open a support ticket requesting additional addresses before attempting allocation.

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


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `state` | <center>`str`</center> | <center>**Required**</center> | The state of this IP.  **(Choices: `present`, `absent`)** |
| `linode_id` | <center>`int`</center> | <center>Optional</center> | The ID of a Linode you have access to that this address will be allocated to.   |
| `public` | <center>`bool`</center> | <center>Optional</center> | Whether to create a public or private IPv4 address.   |
| `type` | <center>`str`</center> | <center>Optional</center> | The type of address you are requesting. Only IPv4 addresses may be allocated through this operation.  **(Choices: `ipv4`)** |
| `address` | <center>`str`</center> | <center>Optional</center> | The IP address to delete.  **(Conflicts With: `linode_id`,`public`,`type`)** |

## Return Values

