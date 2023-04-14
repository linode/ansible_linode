"""Documentation fragments for the type_list module"""

specdoc_examples = ['''
- name: List all of the Linode Instance Types
  linode.cloud.type_list: {}''', '''
- name: List a Linode Instance Type named Nanode 1GB
  linode.cloud.type_list:
    filters:
      - name: label
        values: Nanode 1GB
''']

result_type_samples = ['''[
    {
        "addons": {
            "backups": {
                "price": {
                    "hourly": 0.008,
                    "monthly": 5
                }
            }
        },
        "class": "standard",
        "disk": 81920,
        "gpus": 0,
        "id": "g6-standard-2",
        "label": "Linode 4GB",
        "memory": 4096,
        "network_out": 1000,
        "price": {
            "hourly": 0.03,
            "monthly": 20
        },
        "successor": null,
        "transfer": 4000,
        "vcpus": 2
    }
]''']
