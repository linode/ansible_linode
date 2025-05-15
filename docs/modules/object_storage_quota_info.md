# object_storage_quota_info

Get info about a Linode Object Storage Quota.

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
- name: Get info about an Object Storage quota
  linode.cloud.object_storage_quota_info: 
    quota_id: obj-buckets-us-sea-1.linodeobjects.com
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `quota_id` | <center>`str`</center> | <center>**Required**</center> | The Quota ID of the Object Storage Quota to resolve.   |

## Return Values

- `object_storage_quota` - The returned Object Storage Quota.

    - Sample Response:
        ```json
        {
            "description": "Maximum number of buckets this customer is allowed to have on this endpoint",
            "endpoint_type": "E1",
            "quota_id": "obj-buckets-us-sea-1.linodeobjects.com",
            "quota_limit": 1000,
            "quota_name": "Number of Buckets",
            "resource_metric": "bucket",
            "s3_endpoint": "us-sea-1.linodeobjects.com"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-object-storage-quota) for a list of returned fields


- `quota_usage` - The returned Quota Usage.

    - Sample Response:
        ```json
        {
            "quota_limit": 1000,
            "usage": 0
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-object-storage-quota-usage) for a list of returned fields


