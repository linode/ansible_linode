"""Documentation fragments for the monitor_logs_stream module"""

specdoc_examples = ['''
- name: Create a new monitor logs stream
  linode.cloud.monitor_logs_stream:
    label: "my-audit-logs"
    type: "audit_logs"
    status: "active"
    destinations:
      - 12345
    state: present

- name: Update an existing stream's destinations
  linode.cloud.monitor_logs_stream:
    id: 9876
    label: "my-audit-logs-updated"
    destinations:
      - 54321
    state: present

- name: Delete a monitor logs stream
  linode.cloud.monitor_logs_stream:
    id: 9876
    state: absent
''']

result_stream_samples = [
    '''{
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
    }'''
]
