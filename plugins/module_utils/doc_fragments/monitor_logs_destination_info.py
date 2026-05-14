"""Documentation fragments for the monitor_logs_destination_info module"""

specdoc_examples = ['''
- name: Get info about a logs destination by ID
  linode.cloud.monitor_logs_destination_info:
    id: 12345''','''
- name: Get info about a logs destination by label
  linode.cloud.monitor_logs_destination_info:
    label: 'OBJ_logs_destination''']

result_logs_destination_samples = ['''{
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
}''','''{
  "created": "2025-07-20T09:45:13",
  "created_by": "John Q. Linode",
  "details": {
    "authentication": {
      "details": {
        "basic_authentication_password": "p@$$w0Rd",
        "basic_authentication_user": "John_Q"
      },
      "type": "basic"
    },
    "client_certificate_details": {},
    "content_type": "application/json",
    "custom_headers": [
      {
        "name": "Cache-Control",
        "value": "max-age=0"
      }
    ],
    "data_compression": "gzip",
    "endpoint_url": "https://my-site.com/log-storage/database-info"
  },
  "id": 12346,
  "label": "custom_logs_destination",
  "type": "custom_https",
  "updated": "2025-07-21T12:41:09",
  "updated_by": "Jane Q. Linode"
}''']
