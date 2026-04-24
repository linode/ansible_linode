"""Documentation fragments for the monitor_logs_destination_list module"""

specdoc_examples = ['''
- name: List all of available logs destinations to the account
'''] #fixme

result_logs_destinations_samples = ['''[
    {
      "created": "2025-07-20 09:45:13",
      "created_by": "John Q. Linode",
      "details": {
        "access_key_id": 123,
        "bucket_name": "primary-bucket",
        "host": "primary-bucket-1.us-iad-12.linodeobjects.com",
        "path": "audit-logs-logs"
      },
      "id": 12345,
      "label": "OBJ_logs_destination",
      "status": "active",
      "type": "akamai_object_storage",
      "updated": "2025-07-21 12:41:09",
      "updated_by": "Jane Q. Linode",
      "version": 2
    },
    {
      "created": "2025-07-21 10:30:15",
      "created_by": "Jane Q. Linode",
      "details": {
        "access_key_id": 456,
        "bucket_name": "secondary-bucket",
        "host": "secondary-bucket-1.us-iad-12.linodeobjects.com",
        "path": "audit-logs-backup"
      },
      "id": 12345,
      "label": "OBJ_logs_backup_destination",
      "status": "inactive",
      "type": "akamai_object_storage",
      "updated": "2025-07-21 10:30:15",
      "updated_by": "Jane Q. Linode",
      "version": 1
    }
  ]
''']