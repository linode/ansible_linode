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
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-alert-definition) for a list of returned fields


