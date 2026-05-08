# monitor_logs_destination_info

Get info about a Linode Logs Destination.

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
- name: Get info about a logs destination
  linode.cloud.monitor_logs_destination_info:
    id: 12345
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>**Required**</center> | The ID of the Logs Destination to resolve.   |

## Return Values

- `logs_destination` - The returned Logs Destination.

    - Sample Response:
        ```json
        {
          "created": "2025-07-20 09:45:13",
          "created_by": "John Q. Linode",
          "details": {
            "access_key_id": 123,
            "bucket_name": "primary-bucket",
            "host": "primary-bucket-1.us-iad-12.linodeobjects.com",
            "path": "audit-logs"
          },
          "id": 12345,
          "label": "OBJ_logs_destination",
          "status": "active",
          "type": "akamai_object_storage",
          "updated": "2025-07-21 12:41:09",
          "updated_by": "Jane Q. Linode",
          "version": 1
        }
        ```
        ```json
        {
          "created": "2025-07-20T09:45:13",
          "created_by": "John Q. Linode",
          "details": {
            "authentication": {
              "details": {
                "basic_authentication_password": "p@$$w0Rd",
                "basic_authentication_user": "John_Q"
              },
              "type": "basic"
            },
            "client_certificate_details": {},
            "content_type": "application/json",
            "custom_headers": [
              {
                "name": "Cache-Control",
                "value": "max-age=0"
              }
            ],
            "data_compression": "gzip",
            "endpoint_url": "https://my-site.com/log-storage/database-info"
          },
          "id": 12346,
          "label": "custom_logs_destination",
          "type": "custom_https",
          "updated": "2025-07-21T12:41:09",
          "updated_by": "Jane Q. Linode"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-destination) for a list of returned fields


