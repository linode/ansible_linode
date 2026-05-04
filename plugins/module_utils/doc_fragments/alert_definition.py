"""Documentation fragments for the monitor_services_alert_definition module"""

specdoc_examples = ['''
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
    state: present''',  '''
- name: Delete alert definition
  linode.cloud.monitor_services_alert_definition:
    service_type: 'dbaas'
    id: 123
    state: absent
  register: delete''']

result_aclp_alert_definition_sample = ['''{
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
}''']
