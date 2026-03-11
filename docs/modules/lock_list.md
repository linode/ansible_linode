# lock_list

List and filter on Locks.

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
- name: List all locks for the current account
  linode.cloud.lock_list: {}
```

```yaml
- name: List all locks with a specific lock type
  linode.cloud.lock_list:
    filters:
      - name: lock_type
        values: cannot_delete
```

```yaml
- name: List all locks for a specific entity type
  linode.cloud.lock_list:
    filters:
      - name: entity.type
        values: linode
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Locks in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Locks by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Locks.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Locks to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](TBD).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `locks` - The returned Locks.

    - Sample Response:
        ```json
        [
          {
            "id": 1,
            "lock_type": "cannot_delete_with_subresources",
            "entity": {
              "id": 290349,
              "type": "linode",
              "label": "linode290349",
              "url": "/v4/linode/instances/290349"
            }
          }
        ]
        ```
    - See the [Linode API response documentation](TBD) for a list of returned fields


