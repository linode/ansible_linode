# ip_assign

Assign IPs to Linodes in a given Region.

The following restrictions apply:

 - All Linodes involved must have at least one public IPv4 address after assignment.

 - Linodes may have no more than one assigned private IPv4 address.

 - Linodes may have no more than one assigned IPv6 range.

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
- name: Assign IP to Linode
  linode.cloud.ip_assign:
    region: us-east
    assignments:
     - address: 0.0.0.0
       linode_id: 123
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| [`assignments` (sub-options)](#assignments) | <center>`list`</center> | <center>**Required**</center> | List of assignments to make.  **(Updatable)** |
| `region` | <center>`str`</center> | <center>**Required**</center> | The Region to operate in.   |

### assignments

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `address` | <center>`str`</center> | <center>**Required**</center> | The IPv4 address or IPv6 range.   |
| `linode_id` | <center>`int`</center> | <center>**Required**</center> | ID of the Linode.   |

## Return Values

