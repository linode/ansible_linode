"""Documentation fragments for the object_cluster_list module"""

specdoc_examples = ['''
- name: List all of the object storage clusters for the current Linode Account
  linode.cloud.object_cluster_list: {}''', '''
- name: Resolve all object storage clusters for the current Linode Account
  linode.cloud.object_cluster_list:
    filters:
      - name: region
        values: us-east''']

result_object_clusters_samples = ['''[
  {
    "domain": "us-east-1.linodeobjects.com",
    "id": "us-east-1",
    "region": "us-east",
    "static_site_domain": "website-us-east-1.linodeobjects.com",
    "status": "available"
  }
]''']
