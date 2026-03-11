# lock_info

Get info about a Linode Lock.

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
- name: Get info about a lock by ID
  linode.cloud.lock_info:
    id: 3274
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>**Required**</center> | The ID of the Lock to resolve.   |

## Return Values

- `lock` - The returned Lock.

    - Sample Response:
        ```json
        {
            "id": 1,
            "lock_type": "cannot_delete",
            "entity": {
                "id": 6003234,
                "type": "linode",
                "label": "my-linode",
                "url": "/v4/linode/instances/6003234"
            }
        }
        ```


