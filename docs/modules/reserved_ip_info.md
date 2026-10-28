# reserved_ip_info

Get info about a Linode Reserved IP address.

NOTE: Reserved IP feature may not currently be available to all users.

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
- name: Get info about a reserved IP address
  linode.cloud.reserved_ip_info:
    address: "192.0.2.141"
  register: ip_info
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `address` | <center>`str`</center> | <center>**Required**</center> | The reserved IP address to retrieve information about.   |

## Return Values

- `reserved_ip` - The reserved IP address in JSON serialized form.

    - Sample Response:
        ```json
        {
          "address": "192.0.2.141",
          "assigned_entity": null,
          "gateway": "192.0.2.1",
          "interface_id": null,
          "linode_id": null,
          "prefix": 24,
          "public": true,
          "rdns": "",
          "region": "us-east",
          "reserved": true,
          "subnet_mask": "255.255.255.0",
          "tags": [
            "lb",
            "prod"
          ],
          "type": "ipv4",
          "vpc_nat_1_1": null
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-reserved-ip) for a list of returned fields


