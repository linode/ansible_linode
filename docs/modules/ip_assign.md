# ip_assign

Assign IPs to Linodes in a given Region.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Assign IP to Linode
  linode.cloud.ip_assign:
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

