# instance_interface_settings

Create, read, and update the interface settings for a Linode instance.

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
- name: Configure the interface settings of a Linode Instance
  linode.cloud.instance_interface_settings:
    instance_id: 123
    network_helper: true
    default_route:
        ipv4_interface_id: 123
        ipv6_interface_id: 456

```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `instance_id` | <center>`int`</center> | <center>**Required**</center> | The ID of the instance to configure the interface settngs for.   |
| `network_helper` | <center>`bool`</center> | <center>Optional</center> | Enables the Network Helper feature. The default value is determined by the network_helper setting in the account settings. Power off the Linode before disabling or enabling Network Helper.   |
| [`default_route` (sub-options)](#default_route) | <center>`dict`</center> | <center>Optional</center> | Interfaces used for the IPv4 default_route and IPv6 default_route when multiple interfaces are eligible for the role.   |

### default_route

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `ipv4_interface_id` | <center>`int`</center> | <center>Optional</center> | The VPC or public interface ID assigned as the IPv4 default_route.   |
| `ipv6_interface_id` | <center>`int`</center> | <center>Optional</center> | The VPC or public interface ID assigned as the IPv6 default_route.   |

## Return Values

- `settings` - The Linode interface settings in JSON serialized form.

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


