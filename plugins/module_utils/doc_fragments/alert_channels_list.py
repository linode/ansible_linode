"""Documentation fragments for the monitor_alert_channel_list module"""

specdoc_examples = ['''
- name: List all of available alert channels to the account
  linode.cloud.monitor_alert_channel_list:
    api_version: v4beta''']

result_alert_channels_samples = ['''[
    {
      "alerts": [
        {
          "id": 10000,
          "label": "High Memory Usage Plan Dedicated",
          "type": "alerts-definitions",
          "url": "/monitor/alerts-definitions/10000"
        },
        {
          "id": 10001,
          "label": "High Memory Usage Plan Shared",
          "type": "alerts-definitions",
          "url": "/monitor/alerts-definitions/10001"
        }
      ],
      "channel_type": "email",
      "content": {
        "email": {
          "email_addresses": [
            "Users-with-read-write-access-to-resources"
          ]
        }
      },
      "created": "2025-03-20T01:41:09",
      "created_by": "system",
      "id": 10000,
      "label": "Read-Write Channel",
      "type": "system",
      "updated": "2025-03-20T01:41:09",
      "updated_by": "system"
    }
]
''']
