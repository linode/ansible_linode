"""Documentation fragments for the volume_type_list module"""

specdoc_examples = ['''
- name: List all of the Linode Volume Types
  linode.cloud.volume_type_list: {}''', '''
- name: List a Linode Volume Type named Storage Volume
  linode.cloud.volume_type_list:
    filters:
      - name: label
        values: Storage Volume
''']

result_volume_type_samples = ['''[
    {
        "id": "volume",
        "label": "Storage Volume",
        "price": {
            "hourly": 0.00015,
            "monthly": 0.1
        },
        "region_prices": [
            {
                "id": "id-cgk",
                "hourly": 0.00018,
                "monthly": 0.12
            },
            {
                "id": "br-gru",
                "hourly": 0.00021,
                "monthly": 0.14
            }
        ],
        "transfer": 0
    }
]''']
