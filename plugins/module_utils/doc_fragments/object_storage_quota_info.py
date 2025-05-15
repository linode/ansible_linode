"""Documentation fragments for the object_storage_quota_info module"""

result_object_storage_quota_samples = ['''{
    "description": "Maximum number of buckets this customer is allowed to have on this endpoint",
    "endpoint_type": "E1",
    "quota_id": "obj-buckets-us-sea-1.linodeobjects.com",
    "quota_limit": 1000,
    "quota_name": "Number of Buckets",
    "resource_metric": "bucket",
    "s3_endpoint": "us-sea-1.linodeobjects.com"
}''']

result_object_storage_quota_usage_samples = ['''{
    "quota_limit": 1000,
    "usage": 0
}''']


specdoc_examples = ['''
- name: Get info about an Object Storage quota
  linode.cloud.object_storage_quota_info: 
    quota_id: obj-buckets-us-sea-1.linodeobjects.com''']
