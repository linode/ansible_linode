# instance_interface_settings_info

Get info about a Linode settings.

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
- name: Get the interface settings for an instance by label
  linode.cloud.instance_interface_settings_info:
    label: my-instance
```

```yaml
- name: Get the interface settings for an instance by ID
  linode.cloud.instance_interface_settings_info:
    id: 12345
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the settings to resolve.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the settings to resolve.  **(Conflicts With: `id`)** |

## Return Values

- `settings` - The returned settings.

    - Sample Response:
        ```json
        
        {
          "default_route": {
            "ipv4_eligible_interface_ids": [
              123,
              456
            ],
            "ipv4_interface_id": 456,
            "ipv6_eligible_interface_ids": [
              123
            ],
            "ipv6_interface_id": 123
          },
          "network_helper": true
        }
        
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-linode-interface-settings) for a list of returned fields


