# ip_share

Manage Linode shared IPs.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Configure IPs to share with a Linode.
  linode.cloud.ip_share::
    linode_id: 12345
    ips: ["192.0.2.1", "2001:db8:3c4d:15::"]
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `linode_id` | <center>`int`</center> | <center>Required</center> | The ID of the primary Linode that the addresses will be shared with. |
| `ips` | <center>`[]str`</center> | <center>Required</center> | A list of secondary Linode IPs to share with the primary Linode. |

## Return Values

- `ip_share_stats` - The shared IPs Stats in JSON serialized form.

    - Sample Response:
        ```json
        [
          {
            "ips": [
                "143.42.6.95"
            ],
            "linode_id": 48531373
          }
        ]
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/networking/#ip-addresses-share) for a list of returned fields