# monitor_alert_definition_entities_list

List and filter on Alert Definition Entities.

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
- name: List all entities for a specific alert definition
  linode.cloud.monitor_alert_definition_entities_list:
    service_type: dbaas
    id: 12345
    api_version: v4beta
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `service_type` | <center>`str`</center> | <center>**Required**</center> | The parent Service Type for the Alert Definition Entities.   |
| `id` | <center>`int`</center> | <center>**Required**</center> | The parent Alert Definition for the Alert Definition Entities.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Alert Definition Entities to return. If undefined, all results will be returned.   |

## Return Values

- `alert_definition_entities` - The returned Alert Definition Entities.

    - Sample Response:
        ```json
        [
            {
              "id": "1",
              "label": "mydatabase-1",
              "url": "/v4/databases/mysql/instances/1",
              "type": "dbaas"
            },
            {
              "id": "2",
              "label": "mydatabase-2",
              "url": "/v4/databases/mysql/instances/2",
              "type": "dbaas"
            },
            {
              "id": "3",
              "label": "mydatabase-3",
              "url": "/v4/databases/mysql/instances/3",
              "type": "dbaas"
            }
          ]
        
        ```
    - See the [Linode API response documentation](TODO) for a list of returned fields


