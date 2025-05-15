# object_storage_quota_list

List and filter on Object Storage Quotas.

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
- name: List all of Object Storage Quotas for the current account
  linode.cloud.object_storage_quotas:
    filters:
      - name: s3_endpoint
        values:
          - es-mad-1.linodeobjects.com
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Object Storage Quotas in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Object Storage Quotas by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Object Storage Quotas.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Object Storage Quotas to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-object-storage-quotas).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `object_storage_quotas` - The returned Object Storage Quotas.

    - Sample Response:
        ```json
        [
                {
                    "description": "Maximum number of buckets this customer is allowed to have on this endpoint",
                    "endpoint_type": "E1",
                    "quota_id": "obj-buckets-es-mad-1.linodeobjects.com",
                    "quota_limit": 1000,
                    "quota_name": "Number of Buckets",
                    "resource_metric": "bucket",
                    "s3_endpoint": "es-mad-1.linodeobjects.com"
                },
                {
                    "description": "Maximum number of bytes this customer is allowed to have on this endpoint",
                    "endpoint_type": "E1",
                    "quota_id": "obj-bytes-es-mad-1.linodeobjects.com",
                    "quota_limit": 109951162777600,
                    "quota_name": "Total Capacity",
                    "resource_metric": "byte",
                    "s3_endpoint": "es-mad-1.linodeobjects.com"
                }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-object-storage-quotas) for a list of returned fields


