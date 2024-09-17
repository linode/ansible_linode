# ip_share

Manage the Linode shared IPs.

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
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the target.  **(Choices: `present`, `absent`)** |

## Return Values

- `ip_share_stats` - The Linode IP share info in JSON serialized form

    - Sample Response:
        ```json
        [
          {
            "linode_id": 12345,
            "ips": ["192.0.2.1", "2001:db8:3c4d:15::"]
          }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/post-share-ips) for a list of returned fields


