"""Documentation fragments for the object_storage_global_quota_info module"""

result_object_storage_global_quota_samples = ['''{
    "description": "Current number of access keys per account",
    "has_usage": true,
    "quota_id": "keys",
    "quota_limit": 100,
    "quota_name": "Number of Access Keys",
    "quota_type": "keys",
    "resource_metric": "key"
}''']

result_object_storage_global_quota_usage_samples = ['''{
    "quota_limit": 100,
    "usage": 47
}''']


specdoc_examples = ['''
- name: Get info about an Object Storage global quota
  linode.cloud.object_storage_global_quota_info:
    quota_id: keys''']
