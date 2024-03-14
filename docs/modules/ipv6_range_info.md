# ipv6_range_info

Get info about a Linode IPv6 range.

LINODE_API_TOKEN environment variable is required.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Get info about an IPv6 range
  linode.cloud.ipv6_range_info:
    range: 2600:3c01::
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
    - See the [Linode API response documentation](https://www.linode.com/docs/api/networking/#ipv6-range-view__response-samples) for a list of returned fields


