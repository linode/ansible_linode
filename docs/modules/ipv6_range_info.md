# ipv6_range_info

Get info about a Linode IPv6 range.

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
- name: Get info about an IPv6 range
  linode.cloud.ipv6_range_info:
    range: "2600:3c01::"
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `range` | <center>`str`</center> | <center>Optional</center> | The IPv6 range to access.   |

## Return Values

- `range` - The IPv6 range in JSON serialized form.

    - Sample Response:
        ```json
        {
          "is_bgp": false,
          "linodes": [
            123
          ],
          "prefix": 64,
          "range": "2600:3c01::",
          "region": "us-east"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-ipv6-range) for a list of returned fields


