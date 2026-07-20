# monitor_alert_channel_list

List and filter on Alert Channels.

WARNING! This module makes use of beta endpoints and requires the C(api_version) field be explicitly set to C(v4beta).

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
- name: List all of available alert channels to the account
  linode.cloud.monitor_alert_channel_list:
    api_version: v4beta
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Alert Channels in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Alert Channels by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Alert Channels.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Alert Channels to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-alert-channels).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `alert_channels` - The returned Alert Channels.

    - Sample Response:
        ```json
        [
            {
                "id": 123,
                "label": "alert notification channel",
                "type": "user",
                "channel_type": "email",
                "details": {
                    "email": {
                        "usernames": [
                            "admin-user1",
                            "admin-user2"
                        ],
                        "recipient_type": "user"
                    }
                },
                "alerts": {
                    "url": "/monitor/alert-channels/123/alerts",
                    "type": "alerts-definitions",
                    "alert_count": 0
                },
                "created": "2024-01-01T00:00:00",
                "updated": "2024-01-01T00:00:00",
                "created_by": "tester",
                "updated_by": "tester"
            }
        ]
        
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-alert-channels) for a list of returned fields


