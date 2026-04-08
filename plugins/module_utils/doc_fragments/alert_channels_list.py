"""Documentation fragments for the monitor_alert_channel_list module"""

specdoc_examples = ['''
- name: List all of available alert channels to the account
  linode.cloud.monitor_alert_channel_list:
    api_version: v4beta''']

result_alert_channels_samples = ['''[
    {
        "id": 123,
        "label": "alert notification channel",
        "type": "user",
        "channel_type": "email",
        "details": {
            "email": {
                "usernames": [
                    "admin-user1",
                    "admin-user2"
                ],
                "recipient_type": "user"
            }
        },
        "alerts": {
            "url": "/monitor/alert-channels/123/alerts",
            "type": "alerts-definitions",
            "alert_count": 0
        },
        "created": "2024-01-01T00:00:00",
        "updated": "2024-01-01T00:00:00",
        "created_by": "tester",
        "updated_by": "tester"
    }
]
''']
