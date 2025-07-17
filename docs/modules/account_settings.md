# account_settings

Returns information related to your Account settings.

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
- name: Retrieve
  linode.cloud.account_settings:
    state: present
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `state` | <center>`str`</center> | <center>**Required**</center> | The state of Account Settings.  **(Choices: `present`)** |
| `backups_enabled` | <center>`bool`</center> | <center>Optional</center> | Account-wide backups default. If true, all Linodes created will automatically be enrolled in the Backups service. If false, Linodes will not be enrolled by default, but may still be enrolled on creation or later.   |
| `longview_subscription` | <center>`str`</center> | <center>Optional</center> | The Longview Pro tier you are currently subscribed to. The value must be a Longview subscription ID or null for Longview Free.   |
| `managed` | <center>`bool`</center> | <center>Optional</center> | Our 24/7 incident response service. This robust, multi-homed monitoring system distributes monitoring checks to ensure that your servers remain online and available at all times. Linode Managed can monitor any service or software stack reachable over TCP or HTTP. Once you add a service to Linode Managed, we'll monitor it for connectivity, response, and total request time.   |
| `network_helper` | <center>`bool`</center> | <center>Optional</center> | Enables network helper across all users by default for new Linodes and Linode Configs.   |
| `object_storage` | <center>`str`</center> | <center>Optional</center> | A string describing the status of this account's Object Storage service enrollment.   |

## Return Values

- `account_settings` - Account Settings in JSON serialized form.

    - Sample Response:
        ```json
        {
          "backups_enabled": true,
          "interfaces_for_new_linodes": "linode_only",
          "longview_subscription": "longview-3",
          "managed": true,
          "network_helper": false,
          "object_storage": "active"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-account-settings) for a list of returned fields


