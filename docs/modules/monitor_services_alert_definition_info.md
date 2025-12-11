# monitor_services_alert_definition_info

Get info about a Linode Alert Definition.

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
- linode.cloud.monitor_services_alert_definition_info:
    service_type: 'dbaas'
    id: 12345
    api_version: v4beta
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `service_type` | <center>`str`</center> | <center>**Required**</center> | The ID of the Service Type for this resource.   |
| `id` | <center>`int`</center> | <center>**Required**</center> | The ID of the Alert Definition to resolve.   |

## Return Values

- `alert_definition` - The returned Alert Definition.

    - Sample Response:
        ```json
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
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-alert-definition) for a list of returned fields


