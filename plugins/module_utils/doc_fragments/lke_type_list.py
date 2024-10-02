"""Documentation fragments for the lke_type_list module"""

specdoc_examples = ['''
- name: List all of the Linode LKE Types
  linode.cloud.lke_type_list: {}''', '''
- name: List a Linode LKE Type named LKE High Availability
  linode.cloud.lke_type_list:
    filters:
      - name: label
        values: LKE High Availability
''']

result_lke_type_samples = ['''[
    {
        "id": "lke-ha",
        "label": "LKE High Availability",
        "price": {
            "hourly": 0.09,
            "monthly": 60.0
        },
        "region_prices": [
            {
                "id": "id-cgk",
                "hourly": 0.108,
                "monthly": 72.0
            },
            {
                "id": "br-gru",
                "hourly": 0.126,
                "monthly": 84.0
            }
        ],
        "transfer": 0
    }
]''']
