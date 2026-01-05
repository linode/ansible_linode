# firewall_settings_info

Get info about a Linode Firewall Settings.

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
- name: Update the default firewall settings
  linode.cloud.firewall_settings_info: {}
```


## Return Values

- `firewall_settings` - The returned Firewall Settings.

    - Sample Response:
        ```json
        {
          "default_firewall_ids": {
            "linode": 123456,
            "nodebalancer": 123456,
            "public_interface": 123456,
            "vpc_interface": 123456
          }
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-firewall-settings) for a list of returned fields


