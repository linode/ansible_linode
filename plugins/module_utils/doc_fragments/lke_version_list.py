"""Documentation fragments for the lke_version_list module with tier left unspecified"""

specdoc_examples = ['''
- name: List all Kubernetes versions available for deployment to a Kubernetes cluster
  linode.cloud.lke_version_list: {}
  
- name: List all enterprise-tier Kubernetes versions available for deployment to a Kubernetes cluster
  linode.cloud.lke_version_list: {tier: "enterprise"}
''']

result_lke_versions_samples = ['''
# Result for listing all Kubernetes versions
[
    {
        "id": "1.32"
    },
    {
        "id": "1.31"
    },
    {
        "id": "1.30"
    }
]
# Result for listing all enterprise-tier Kubernetes versions
[
    {
        "id": "v1.31.1+lke1",
        "tier": "enterprise"
    }
]
''']
