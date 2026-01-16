# monitor_services_alert_definition

Manage an alert definition for a specific service type. Akamai refers to these as user alerts. You need read_only access to the scope for the selected serviceType. 

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
- name: Create an alert definition for a service type (dbaas)
  linode.cloud.monitor_services_alert_definition:
    service_type: 'dbaas'
    description: 'An alert definition for ansible test.'
    label: 'ansible-test'
    severity: 1
    rule_criteria:
      rules:
        - aggregate_function: 'avg'
          dimension_filters:
            - dimension_label: 'node_type'
              label: 'Node Type'
              operator: 'eq'
              value: 'primary'
          label: 'Memory Usage'
          metric: 'memory_usage'
          operator: 'gt'
          threshold: 90
          unit: 'percent'
    trigger_conditions:
      criteria_condition: 'ALL'
      evaluation_period_seconds: 300
      polling_interval_seconds: 300
      trigger_occurrences: 1
    channel_ids: '{{ alert_channels }}'
    state: present
```

```yaml
- name: Delete alert definition
  linode.cloud.monitor_services_alert_definition:
    service_type: 'dbaas'
    id: 123
    state: absent
  register: delete
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `service_type` | <center>`str`</center> | <center>**Required**</center> | The Akamai Cloud Computing service being monitored.   |
| `channel_ids` | <center>`list`</center> | <center>**Required**</center> | The identifiers for the alert channels to use for the alert. Run the List alert channels operation and store the id for the applicable channels.  **(Updatable)** |
| `label` | <center>`str`</center> | <center>**Required**</center> | The name of the alert definition. This is used for display purposes in Akamai Cloud Manager.  **(Updatable)** |
| [`rule_criteria` (sub-options)](#rule_criteria) | <center>`dict`</center> | <center>**Required**</center> | Details for the rules required to trigger the alert.  **(Updatable)** |
| `severity` | <center>`int`</center> | <center>**Required**</center> | The severity of the alert. Supported values include 3 for info, 2 for low, 1 for medium, and 0 for severe.  **(Choices: `0`, `1`, `2`, `3`; Updatable)** |
| [`trigger_conditions` (sub-options)](#trigger_conditions) | <center>`dict`</center> | <center>**Required**</center> | The conditions that need to be met to send a notification for the alert.  **(Updatable)** |
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the target.  **(Choices: `present`, `absent`)** |
| `description` | <center>`str`</center> | <center>Optional</center> | An additional description for the alert definition.  **(Updatable)** |
| `entity_ids` | <center>`list`</center> | <center>Optional</center> | The id for each individual entity from a service_type. Get this value by running the list operation for the appropriate entity. For example, if your entity is one of your PostgreSQL databases, run the List PostgreSQL Managed Databases operation and store the id for the appropriate database from the response. You also need read_only access to the scope for the service_type for each of the entity_ids.  **(Updatable)** |
| `id` | <center>`int`</center> | <center>Optional</center> | The unique identifier assigned to the alert definition. Run the List alert definitions operation and store the id for the applicable alert definition. Required for updating.   |
| `status` | <center>`str`</center> | <center>Optional</center> | The current status of the alert.  **(Choices: `enabled`, `disabled`; Updatable)** |
| `wait` | <center>`bool`</center> | <center>Optional</center> | Wait for the alert definition ready (not in progress).  **(Default: `False`)** |
| `wait_timeout` | <center>`int`</center> | <center>Optional</center> | The amount of time, in seconds, to wait for the alert definition.  **(Default: `600`)** |

### rule_criteria

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| [`rules` (sub-options)](#rules) | <center>`list`</center> | <center>Optional</center> | The individual rules that make up the alert definition.   |

### rules

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `aggregate_function` | <center>`str`</center> | <center>Optional</center> | The aggregation function applied to the metric.  **(Choices: `avg`, `sum`, `min`, `max`)** |
| [`dimension_filters` (sub-options)](#dimension_filters) | <center>`list`</center> | <center>Optional</center> | Individual objects that define dimension filters for the rule.   |
| `metric` | <center>`str`</center> | <center>Optional</center> | The metric to query.   |
| `operator` | <center>`str`</center> | <center>Optional</center> | The operator to apply to the metric. Available values are eq for equal, gt for greater than, lt for less than, gte for greater than or equal, and lte for less than or equal.  **(Choices: `eq`, `gt`, `lt`, `gte`, `lte`)** |
| `threshold` | <center>`float`</center> | <center>Optional</center> | The predefined value or condition that triggers an alert when met or exceeded.   |

### dimension_filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `dimension_label` | <center>`str`</center> | <center>Optional</center> | The name of the dimension to be used in the filter.   |
| `operator` | <center>`str`</center> | <center>Optional</center> | The operator to apply to the dimension filter. Available values are eq for equal, neq for not equal, startswith, and endswith.  **(Choices: `eq`, `neq`, `startswith`, `endswith`)** |
| `value` | <center>`str`</center> | <center>Optional</center> | The value to compare the dimension_label against.   |

### trigger_conditions

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `criteria_condition` | <center>`str`</center> | <center>Optional</center> | Signifies the logical operation applied when multiple metrics are set for an alert definition. For example, if you wanted to apply both cpu_usage > 90 and memory_usage > 80, ALL is the criteria_condition. Currently, only ALL is supported.  **(Choices: `ALL`)** |
| `evaluation_period_seconds` | <center>`int`</center> | <center>Optional</center> | The time period over which data is collected before evaluating whether the alert definition's threshold has been met or exceeded.   |
| `polling_interval_seconds` | <center>`int`</center> | <center>Optional</center> | The frequency at which the metric is checked for a change in state. For example, with cpu_usage set as your metric and this set to 300, your cpu_usage is checked every 5 minutes for some change in its state.   |
| `trigger_occurrences` | <center>`int`</center> | <center>Optional</center> | The minimum number of consecutive polling_interval_seconds periods that the threshold needs to be breached to trigger the alert.   |

## Return Values

- `alert_definition` - The alert definition in JSON serialized form.

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


