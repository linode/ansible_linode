"""Documentation fragments for the monitor_logs_stream_list module"""

specdoc_examples = ['''
- name: List all logs streams
  linode.cloud.monitor_logs_stream_list:''', '''
- name: List logs streams with active status
  linode.cloud.monitor_logs_stream_list:
    filters:
      - name: status
        values:
          - active''']

result_streams_samples = [
    '''[
      {
        "created": "2025-03-20 01:41:09",
        "created_by": "John Q. Linode",
        "destinations": [
          {
            "details": {
              "access_key_id": "123",
              "bucket_name": "primary-bucket",
              "host": "primary-bucket-1.us-iad-12.linodeobjects.com",
              "path": "audit-logs"
            },
            "id": 12345,
            "label": "OBJ_logs_destination",
            "type": "akamai_object_storage"
          }
        ],
        "id": 12345,
        "label": "AuditLog-config",
        "status": "active",
        "type": "audit_logs",
        "updated": "2025-03-20 01:41:09",
        "updated_by": "Jane Q. Linode",
        "version": 1
      }
    ]'''
]
