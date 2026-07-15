# object_storage_global_quota_info

Get info about a Linode Object Storage Global Quota.

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
- name: Get info about an Object Storage global quota
  linode.cloud.object_storage_global_quota_info:
    quota_id: keys
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `quota_id` | <center>`str`</center> | <center>**Required**</center> | The Quota ID of the Object Storage Global Quota to resolve.   |

## Return Values

- `object_storage_global_quota` - The returned Object Storage Global Quota.

    - Sample Response:
        ```json
        {
            "description": "Current number of access keys per account",
            "has_usage": true,
            "quota_id": "keys",
            "quota_limit": 100,
            "quota_name": "Number of Access Keys",
            "quota_type": "keys",
            "resource_metric": "key"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-object-storage-global-quota) for a list of returned fields


- `quota_usage` - The returned Quota Usage.

    - Sample Response:
        ```json
        {
            "quota_limit": 100,
            "usage": 47
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-object-storage-global-quota-usage) for a list of returned fields


