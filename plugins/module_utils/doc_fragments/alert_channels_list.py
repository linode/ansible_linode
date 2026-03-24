"""Documentation fragments for the monitor_alert_channel_list module"""

specdoc_examples = ['''
- name: List all of available alert channels to the account
  linode.cloud.monitor_alert_channel_list:
    api_version: v4beta''']

result_alert_channels_samples = ['''[
    {
      "id": 10000,
      "label": "Read-Write Channel",
      "channel_type": "email",
      "type": "system",
      "content": {
        "email": {
          "email_addresses": [
            "Users-with-read-write-access-to-resources"
          ]
        }
      },
      "details": {
        "email": {
          "usernames": [],
          "recipient_type": "read_write_users"
        }
      },
      "alerts": {
        "url": "/monitor/alert-channels/10000/alerts",
        "type": "alerts-definitions",
        "alert_count": 8
      },
      "created": "2025-03-20T01:41:09",
      "updated": "2025-03-20T01:41:09",
      "created_by": "system",
      "updated_by": "system"
    }
  ]
''']
