# monitor_services_alert_definition_list

List and filter on Alert Definitions.

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
- name: List all of available alert definitions to the account
  linode.cloud.monitor_services_alert_definition_list:
    api_version: v4beta
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Alert Definitions in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Alert Definitions by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Alert Definitions.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Alert Definitions to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-alert-definitions).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `alert_definitions` - The returned Alert Definitions.

    - Sample Response:
        ```json
        [
            {
              "id": 12345,
              "label": "Test Alert for DBAAS",
              "service_type": "dbaas",
              "severity": 1,
              "type": "user",
              "description": "A test alert for dbaas service",
              "scope": "entity",
              "regions": [],
              "entities": {
                "url": "/monitor/services/dbaas/alert-definitions/12345/entities",
                "count": 1,
                "has_more_resources": false
              },
              "alert_channels": [
                {
                  "id": 10000,
                  "label": "Read-Write Channel",
                  "type": "email",
                  "url": "/monitor/alert-channels/10000"
                }
              ],
              "rule_criteria": {
                "rules": [
                  {
                    "aggregate_function": "avg",
                    "dimension_filters": [
                      {
                        "dimension_label": "node_type",
                        "label": "Node Type",
                        "operator": "eq",
                        "value": "primary"
                      }
                    ],
                    "label": "High CPU Usage",
                    "metric": "cpu_usage",
                    "operator": "gt",
                    "threshold": 90,
                    "unit": "percent"
                  }
                ]
              },
              "trigger_conditions": {
                "criteria_condition": "ALL",
                "evaluation_period_seconds": 300,
                "polling_interval_seconds": 60,
                "trigger_occurrences": 3
              },
              "class": "alert",
              "status": "active",
              "created": "2024-01-01T00:00:00",
              "updated": "2024-01-01T00:00:00",
              "updated_by": "tester"
            }
          ]
        
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-alert-definitions) for a list of returned fields


