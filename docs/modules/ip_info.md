# ip_info

Get info about a Linode IP.

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
- name: Get info about an IP address
  linode.cloud.ip_info:
    address: 97.107.143.141
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `address` | <center>`str`</center> | <center>**Required**</center> | The IP address to operate on.   |

## Return Values

- `ip` - The IP in JSON serialized form.

    - Sample Response:
        ```json
        {
          "address": "97.107.143.141",
          "gateway": "97.107.143.1",
          "linode_id": 123,
          "prefix": 24,
          "public": true,
          "rdns": "test.example.org",
          "region": "us-east",
          "subnet_mask": "255.255.255.0",
          "type": "ipv4",
          "vpc_nat_1_1": {
            "vpc_id": 242,
            "subnet_id": 194,
            "address": "139.144.244.36"
          }
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-ip) for a list of returned fields


