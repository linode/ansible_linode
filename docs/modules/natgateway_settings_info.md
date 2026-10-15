# natgateway_settings_info

Get info about a Linode NAT Gateway Settings.

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
- name: Get info about the current NAT Gateway settings
  linode.cloud.natgateway_settings_info: {}
```


## Return Values

- `settings` - The returned NAT Gateway Settings.

    - Sample Response:
        ```json
        {
          "allowed_ports_per_interface": [
            4096,
            8192,
            16384
          ],
          "maximum_autoscaling_addresses_per_natgateway": 100,
          "maximum_reserved_addresses_per_natgateway": 100
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-natgateway-settings) for a list of returned fields


