# firewall_settings

Configure the firewall settings for the account.

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
  linode.cloud.firewall_settings:
    default_firewall_ids:
      linode: 123456
      nodebalancer: 123456
      public_interface: 123456
      vpc_interface: 123456
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| [`default_firewall_ids` (sub-options)](#default_firewall_ids) | <center>`dict`</center> | <center>Optional</center> | The default firewall ID for a `linode`, `nodebalancer`, `public_interface`, or `vpc_interface`. Default firewalls can't be deleted or disabled.  **(Updatable)** |
| `state` | <center>`str`</center> | <center>Optional</center> | The desired state of the target.  **(Choices: `present`)** |

### default_firewall_ids

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `linode` | <center>`int`</center> | <center>Optional</center> | The Linode's default firewall.   |
| `nodebalancer` | <center>`int`</center> | <center>Optional</center> | The NodeBalancer's default firewall.   |
| `public_interface` | <center>`int`</center> | <center>Optional</center> | The public interface's default firewall.   |
| `vpc_interface` | <center>`int`</center> | <center>Optional</center> | The VPC interface's default firewall.   |

## Return Values

- `default_firewall_ids` - The default firewall ID for a `linode`, `nodebalancer`, `public_interface`, or `vpc_interface`. Default firewalls can't be deleted or disabled.

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
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/put-firewall-settings) for a list of returned fields


