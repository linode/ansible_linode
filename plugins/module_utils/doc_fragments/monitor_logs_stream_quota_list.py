"""Documentation fragments for the monitor_logs_stream_quota_list module"""

specdoc_examples = ['''
- name: List all available monitor logs stream quotas for the account
  linode.cloud.monitor_logs_stream_quota_list: {}''']

result_stream_quotas_samples = ['''[
  {
    "quota_id": "aclp_audit_logs_streams",
    "quota_name": "Number of Audit Logs Streams",
    "description": "Current number of audit logs streams per account",
    "quota_limit": 5,
    "quota_type": "logs_streams_aclp_audit_logs_streams"
  },
  {
    "quota_id": "aclp_lke_audit_logs_streams",
    "quota_name": "Number of LKE Audit Logs Streams",
    "description": "Current number of LKE audit logs streams per account",
    "quota_limit": 10,
    "quota_type": "logs_streams_aclp_lke_audit_logs_streams"
  }
]''']
