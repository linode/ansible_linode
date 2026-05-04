"""Documentation fragments for the monitor_logs_destination module"""

specdoc_examples = ['''
- name: Create a logs destination
  linode.cloud.monitor_logs_destination:
    label: 'test-logs-destination'
    type: 'akamai_object_storage'
    details:
      access_key_id: '{{ access_key_id }}'
      access_key_secret: '{{ access_key_secret }}'
      bucket_name: '{{ bucket_name }}'
      host: '{{ host }}'
      path: 'test-path'
    state: present''', '''
- name: Delete logs destination
  linode.cloud.monitor_logs_destination:
    id: 12345
    state: absent''']

result_logs_destination_sample = ['''{
  "created": "2025-07-20 09:45:13",
  "created_by": "John Q. Linode",
  "details": {
    "access_key_id": 123,
    "bucket_name": "primary-bucket",
    "host": "primary-bucket-1.us-iad-12.linodeobjects.com",
    "path": "audit-logs"
  },
  "id": 12345,
  "label": "OBJ_logs_destination",
  "status": "active",
  "type": "akamai_object_storage",
  "updated": "2025-07-21 12:41:09",
  "updated_by": "Jane Q. Linode",
  "version": 1
}''']
