# placement_group

Manage a Linode Placement Group.

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
- name: Create a placement group
  linode.cloud.placement_group:
    label: my-pg
    region: us-east
    affinity_type: anti_affinity:local
    is_strict: True
    state: present
```

```yaml
- name: Update a placement group label
  linode.cloud.placement_group:
    label: my-pg-updated
    region: us-east
    affinity_type: anti_affinity:local
    is_strict: True
    state: present
```

```yaml
- name: Delete a placement group
  linode.cloud.placement_group:
    label: my-pg
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | <center>`str`</center> | <center>**Required**</center> | The label of the Placement Group. This field can only contain ASCII letters, digits and dashes.   |
| `region` | <center>`str`</center> | <center>Optional</center> | The region that the placement group is in.   |
| `affinity_type` | <center>`str`</center> | <center>Optional</center> | The affinity policy for Linodes in a placement group.   |
| `is_strict` | <center>`bool`</center> | <center>Optional</center> | Whether Linodes must be able to become compliant during assignment.  **(Default: `False`)** |

## Return Values

- `placement_group` - The Placement Group in JSON serialized form.

    - Sample Response:
        ```json
        {
          "id": 123,
          "label": "my-pg",
          "region": "eu-west",
          "affinity_type": "anti_affinity:local",
          "is_strict": true,
          "is_compliant": true,
          "members": [
            {
              "linode_id": 123,
              "is_compliant": true
            }
          ]
        }
        ```
    - See the [Linode API response documentation](TBD) for a list of returned fields


