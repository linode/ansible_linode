# monitor_logs_stream_quota_list

List Monitor Logs Stream Quotas.

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
- name: List all available monitor logs stream quotas for the account
  linode.cloud.monitor_logs_stream_quota_list: {}
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Monitor Logs Stream Quotas to return. If undefined, all results will be returned.   |

## Return Values

- `stream_quotas` - The returned Monitor Logs Stream Quotas.

    - Sample Response:
        ```json
        [
          {
            "quota_id": "aclp_audit_logs_streams",
            "quota_name": "Number of Audit Logs Streams",
            "description": "Current number of audit logs streams per account",
            "quota_limit": 5,
            "quota_type": "logs_streams_aclp_audit_logs_streams"
          },
          {
            "quota_id": "aclp_lke_audit_logs_streams",
            "quota_name": "Number of LKE Audit Logs Streams",
            "description": "Current number of LKE audit logs streams per account",
            "quota_limit": 10,
            "quota_type": "logs_streams_aclp_lke_audit_logs_streams"
          }
        ]
        ```
    - See the [Linode API response documentation](TODO) for a list of returned fields

