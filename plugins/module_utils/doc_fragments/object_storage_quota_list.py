"""Documentation fragments for the object_storage_quota_list module"""

specdoc_examples = ['''
- name: List all of Object Storage Quotas for the current account
  linode.cloud.object_storage_quotas:
    filters:
      - name: s3_endpoint
        values:
          - es-mad-1.linodeobjects.com''']

result_object_storage_quotas_samples = ['''[
        {
            "description": "Maximum number of buckets this customer is allowed to have on this endpoint",
            "endpoint_type": "E1",
            "quota_id": "obj-buckets-es-mad-1.linodeobjects.com",
            "quota_limit": 1000,
            "quota_name": "Number of Buckets",
            "resource_metric": "bucket",
            "s3_endpoint": "es-mad-1.linodeobjects.com"
        },
        {
            "description": "Maximum number of bytes this customer is allowed to have on this endpoint",
            "endpoint_type": "E1",
            "quota_id": "obj-bytes-es-mad-1.linodeobjects.com",
            "quota_limit": 109951162777600,
            "quota_name": "Total Capacity",
            "resource_metric": "byte",
            "s3_endpoint": "es-mad-1.linodeobjects.com"
        }
]''']
