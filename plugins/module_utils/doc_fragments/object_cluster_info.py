"""Documentation fragments for the object_cluster_info module"""

specdoc_examples = ['''
- name: Get info about clusters in us-east
  linode.cloud.object_cluster_info:
    region: us-east''', '''
- name: Get info about the cluster with id us-east-1
  linode.cloud.object_cluster_info:
    id: us-east-1''']

result_clusters_samples = ['''[
  {
    "domain": "us-east-1.linodeobjects.com",
    "id": "us-east-1",
    "region": "us-east",
    "static_site_domain": "website-us-east-1.linodeobjects.com",
    "status": "available"
  }
]''']
