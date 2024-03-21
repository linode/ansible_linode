# ip_share

Manage the Linode shared IPs.

**:warning: This module makes use of beta endpoints and requires the `api_version` field be explicitly set to `v4beta`.**

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Configure the Linode shared IPs.
  linode.cloud.ip_share:
    api_version: v4beta
    linode_id: 12345
    ips: ["192.0.2.1", "2001:db8:3c4d:15::"]
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `ips` | <center>`list`</center> | <center>**Required**</center> | A list of secondary Linode IPs to share with the primary Linode.   |
| `linode_id` | <center>`int`</center> | <center>**Required**</center> | The ID of the primary Linode that the addresses will be shared with.   |

## Return Values

- `ip_share_stats` - The Linode IP share info in JSON serialized form

    - Sample Response:
        ```json
        [
          {
            "linode_id": 12345,
            "ips": ["192.0.2.1", "2001:db8:3c4d:15::"],
          }
        ]
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/networking/#ip-addresses-share__response-samples) for a list of returned fields


