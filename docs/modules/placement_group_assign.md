# placement_group_assign

Manages a single assignment between a Linode and a Placement Group.

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
- name: Assign a Linode to a placement group
  linode.cloud.placement_group_assign:
    placement_group_id: 123
    linode_id: 111
    state: present
```

```yaml
- name: Unassign a Linode from a placement group
  linode.cloud.placement_group_assign:
    placement_group_id: 123
    linode_id: 111
    state: absent

```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `placement_group_id` | <center>`int`</center> | <center>**Required**</center> | The ID of the Placement Group for this assignment.   |
| `linode_id` | <center>`int`</center> | <center>**Required**</center> | The Linode ID to assign or unassign to the Placement Group.   |
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the target.  **(Choices: `present`, `absent`)** |

## Return Values

