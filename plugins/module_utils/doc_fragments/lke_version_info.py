"""Documentation fragments for the lke_version_info module"""

specdoc_examples = [
    '''
    - name: Get info about an LKE version by ID
      linode.cloud.lke_cluster_info:
        id: '1.31'
    ''', '''
    - name: Get info about an LKE version by tier and ID
      linode.cloud.lke_cluster_info:
        tier: 'standard'
        id: '1.31'
    '''
]

result_lke_version_samples = [
    '''
    {
      "id": "1.31"
    }
    ''',
    '''
    {
      "id": "1.31",
      "tier": "standard"
    }
    '''
]
