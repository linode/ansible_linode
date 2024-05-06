# placement_group_info

Get info about a Linode Placement Group.

**:warning: This module makes use of beta endpoints and requires the `api_version` field be explicitly set to `v4beta`.**

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
- name: Get info about a Linode placement group
  linode.cloud.placement_group_info: 
    api_version: v4beta
    id: 123

```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>**Required**</center> | The ID of the Placement Group to resolve.   |

## Return Values

- `placement_group` - The returned Placement Group.

    - Sample Response:
        ```json
        
        {
          "id": 123,
          "label": "test",
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


