"""Documentation fragments for the monitor_alert_definition_entities_list module"""

specdoc_examples = ['''
- name: List all entities for a specific alert definition
  linode.cloud.monitor_alert_definition_entities_list:
    service_type: dbaas
    id: 12345
    api_version: v4beta''']

result_alert_definition_entities_samples = ['''[
    {
      "id": "1",
      "label": "mydatabase-1",
      "url": "/v4/databases/mysql/instances/1",
      "type": "dbaas"
    },
    {
      "id": "2",
      "label": "mydatabase-2",
      "url": "/v4/databases/mysql/instances/2",
      "type": "dbaas"
    },
    {
      "id": "3",
      "label": "mydatabase-3",
      "url": "/v4/databases/mysql/instances/3",
      "type": "dbaas"
    }
  ]
''']
