"""Documentation fragments for the monitor_logs_stream_info module"""

specdoc_examples = ['''
- name: Get info about a logs stream by ID
  linode.cloud.monitor_logs_stream_info:
    id: 12345

- name: Get info about a logs stream by label
  linode.cloud.monitor_logs_stream_info:
    label: "my-audit-logs"
''']
