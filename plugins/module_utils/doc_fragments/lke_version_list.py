"""Documentation fragments for the lke_version_list module"""

specdoc_examples = [
    '''
    - name: List all Kubernetes versions available for deployment to a Kubernetes cluster
      linode.cloud.lke_version_list:
    ''', '''
    - name: List all enterprise-tier Kubernetes versions available for deployment to a Kubernetes cluster
      linode.cloud.lke_version_list:
        tier: "enterprise"
    '''
]

result_lke_versions_samples = [
    '''
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
    ''',
    '''
    [
        {
            "id": "v1.31.1+lke1",
            "tier": "enterprise"
        }
    ]
    '''
]
