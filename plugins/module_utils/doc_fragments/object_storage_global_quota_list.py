"""Documentation fragments for the object_storage_global_quota_list module"""

specdoc_examples = ['''
- name: List all Object Storage global quotas for the current account
  linode.cloud.object_storage_global_quota_list:''']

result_object_storage_global_quotas_samples = ['''[
    {
        "description": "Current number of access keys per account",
        "has_usage": true,
        "quota_id": "keys",
        "quota_limit": 100,
        "quota_name": "Number of Access Keys",
        "quota_type": "keys",
        "resource_metric": "key"
    }
]''']
