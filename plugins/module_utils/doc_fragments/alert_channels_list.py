"""Documentation fragments for the monitor_alert_channel_list module"""

specdoc_examples = ['''
- name: List all of available alert channels to the account
  linode.cloud.monitor_alert_channel_list:
    api_version: v4beta''']

result_alert_channels_samples = ['''[
    {
      "alerts": {
        "alert_count": 5,
        "type": "alerts-definitions",
        "url": "/monitor/alerts-definitions/10000"
      },
      "channel_type": "email",
      "created": "2025-03-20 01:41:09",
      "created_by": "johndoe",
      "details": {
        "email": {
          "recipient_type": "user",
          "usernames": [
            "johndoe",
            "janedoe"
          ]
        }
      },
      "id": 10000,
      "label": "Notification channel #1",
      "type": "user",
      "updated": "2025-03-20 01:41:09",
      "updated_by": "johndoe"
    },
    {
      "alerts": {
        "alert_count": 3,
        "type": "alerts-definitions",
        "url": "/monitor/alert-channels/10001/alerts"
      },
      "channel_type": "email",
      "content": {
        "email": {
          "email_addresses": [
            "Users-with-read-write-access-to-resources"
          ]
        }
      },
      "created": "2025-03-20 01:41:09",
      "created_by": "system",
      "details": {
        "email": {
          "recipient_type": "read_write_users",
          "usernames": []
        }
      },
      "id": 10001,
      "label": "Read-Write Channel",
      "type": "system",
      "updated": "2025-03-20 01:41:09",
      "updated_by": "system"
    }
]
''']
