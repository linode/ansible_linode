"""Documentation fragments for the lke_version_list module"""

specdoc_examples = ['''
- name: List all Kubernetes versions available for deployment to a Kubernetes cluster
  linode.cloud.lke_versions: {}''']

result_lke_versions_samples = ['''[
    {
      "id": "1.25"
    }
]''']
