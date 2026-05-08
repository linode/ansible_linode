"""Documentation fragments for the monitor_logs_destination module"""

specdoc_examples = ['''
- name: Create logs destination with akamai object storage type
  linode.cloud.monitor_logs_destination:
    label: 'test-logs-destination'
    type: 'akamai_object_storage'
    details:
      access_key_id: '{{ access_key_id }}'
      access_key_secret: '{{ access_key_secret }}'
      bucket_name: '{{ bucket_name }}'
      host: '{{ host }}'
      path: 'test-path'
    state: present''','''
- name: Create logs destination with custom https endpoint type
  linode.cloud.monitor_logs_destination:
    label: 'test-logs-destination'
    type: 'custom_https'
    details:
      authentication:
        type: 'basic'
        details:
          basic_authentication_user: '{{ basic_authentication_user }}'
          basic_authentication_password: '{{ basic_authentication_password }}'
      client_certificate_details: 
        client_certificate: '{{ client_certificate }}'
        client_ca_certificate: '{{ client_ca_certificate }}'
        client_private_key: '{{ client_private_key }}'
        tls_hostname: 'my-site.com'
      content_type: 'application/json'
      custom_headers:
        - name: 'Cache-Control'
          value: 'max-age=0'
      data_compression: 'gzip'
      endpoint_url: 'https://my-site.com/log-storage/basicAuth'
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