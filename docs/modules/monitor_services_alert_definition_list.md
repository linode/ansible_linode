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
              "alert_channels": [
                {
                  "id": 10000,
                  "label": "Read-Write Channel",
                  "type": "alert-channels",
                  "url": "/monitor/alert-channels/10000"
                }
              ],
              "class": "dedicated",
              "created": "2025-03-20T01:42:11",
              "created_by": "system",
              "description": "Alert triggers when dedicated plan nodes consistently reach critical memory usage, risking application performance degradation.",
              "entity_ids": [
                "126905",
                "126906",
                "137435",
                "141496",
                "190003",
                "257625",
                "257626"
              ],
              "has_more_resources": false,
              "id": 10000,
              "label": "High Memory Usage Plan Dedicated",
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
                    "label": "Memory Usage",
                    "metric": "memory_usage",
                    "operator": "gt",
                    "threshold": 95,
                    "unit": "percent"
                  }
                ]
              },
              "service_type": "dbaas",
              "severity": 2,
              "status": "enabled",
              "trigger_conditions": {
                "criteria_condition": "ALL",
                "evaluation_period_seconds": 300,
                "polling_interval_seconds": 300,
                "trigger_occurrences": 3
              },
              "type": "system",
              "updated": "2025-03-20T01:42:11",
              "updated_by": "system"
            },
            {
              "alert_channels": [
                {
                  "id": 10000,
                  "label": "Read-Write Channel",
                  "type": "alert-channels",
                  "url": "/monitor/alert-channels/10000"
                }
              ],
              "class": null,
              "created": "2025-03-20T02:15:18",
              "created_by": "John Q. Linode",
              "description": "Custom alert set up for high memory usage for shared plan nodes.",
              "entity_ids": [
                "126907",
                "126908",
                "137436",
                "141497",
                "190004",
                "257627",
                "257628"
              ],
              "has_more_resources": false,
              "id": 10001,
              "label": "High Memory Usage Plan Shared",
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
                    "label": "Memory Usage",
                    "metric": "memory_usage",
                    "operator": "gt",
                    "threshold": 95,
                    "unit": "percent"
                  }
                ]
              },
              "service_type": "dbaas",
              "severity": 2,
              "status": "enabled",
              "trigger_conditions": {
                "criteria_condition": "ALL",
                "evaluation_period_seconds": 300,
                "polling_interval_seconds": 300,
                "trigger_occurrences": 3
              },
              "type": "user",
              "updated": "2025-03-20T02:15:18",
              "updated_by": "John Q. Linode"
            }
          ]
        
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-alert-definitions) for a list of returned fields


