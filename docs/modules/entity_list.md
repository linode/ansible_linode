# entity_list

List Entities.

WARNING! This module makes use of beta endpoints and requires the C(api_version) field be explicitly set to C(v4beta).

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
- name: List all entities for the current account
  linode.cloud.entity_list: {}
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Entities to return. If undefined, all results will be returned.   |

## Return Values

- `entities` - The returned Entities.

    - Sample Response:
        ```json
        [
          {
            "id": 123,
            "label": "my-linode",
            "type": "linode"
          }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-entities) for a list of returned fields


