"""Documentation fragments for the monitor_services_alert_definition_info module"""

specdoc_examples = ['''
- linode.cloud.monitor_services_alert_definition_info:
    service_type: 'dbaas'
    id: 12345
    api_version: v4beta''']

result_alert_definition_samples = ['''{
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
}''']
