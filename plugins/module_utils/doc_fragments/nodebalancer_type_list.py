"""Documentation fragments for the nodebalancer_type_list module"""

specdoc_examples = ['''
- name: List all of the Linode Node Balancer Types
  linode.cloud.nodebalancer_type_list: {}''', '''
- name: List a Linode Node Balancer Type named NodeBalancer
  linode.cloud.nodebalancer_type_list:
    filters:
      - name: label
        values: NodeBalancer
''']

result_nodebalancer_type_samples = ['''[
    {
        "id": "nodebalancer",
        "label": "NodeBalancer",
        "price": {
            "hourly": 0.015,
            "monthly": 10.0
        },
        "region_prices": [
            {
                "id": "id-cgk",
                "hourly": 0.018,
                "monthly": 12.0
            },
            {
                "id": "br-gru",
                "hourly": 0.021,
                "monthly": 14.0
            }
        ],
        "transfer": 0
    }
]''']
