# object_storage_global_quota_list

List Object Storage Global Quotas.

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
- name: List all Object Storage global quotas for the current account
  linode.cloud.object_storage_global_quota_list:
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Object Storage Global Quotas to return. If undefined, all results will be returned.   |

## Return Values

- `object_storage_global_quotas` - The returned Object Storage Global Quotas.

    - Sample Response:
        ```json
        [
            {
                "description": "Current number of access keys per account",
                "has_usage": true,
                "quota_id": "keys",
                "quota_limit": 100,
                "quota_name": "Number of Access Keys",
                "quota_type": "keys",
                "resource_metric": "key"
            }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-object-storage-global-quotas) for a list of returned fields


