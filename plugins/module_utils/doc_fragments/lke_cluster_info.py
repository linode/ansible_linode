"""Documentation fragments for the lke_cluster_info module"""

examples = ['''
- name: Get info about an LKE cluster by label
  linode.cloud.lke_cluster_info:
    label: 'my-cluster' ''', '''
- name: Get info about an LKE cluster by ID
  linode.cloud.lke_cluster_info:
    id: 12345''']
