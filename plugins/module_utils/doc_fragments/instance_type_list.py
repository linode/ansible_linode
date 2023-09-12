"""Documentation fragments for the instance_type_list module"""

specdoc_examples = ['''
- name: List all of the Linode instance types
  linode.cloud.instance_type_list: {}''', '''
- name: Resolve all Linode instance types
  linode.cloud.instance_type_list:
    filters:
      - name: class
        values: nanode''']

result_instance_type_samples = ['''[
   {
      "addons": {
        "backups": {
          "price": {
            "hourly": 0.008,
            "monthly": 5
          },
          "region_prices": [
            {
              "id": "ap-west",
              "hourly": 0.02,
              "monthly": 20
            },
            {
          	  "id": "ap-northeast",
              "hourly": 0.02,
              "monthly": 20
            }
          ]
        }
      },
      "region_prices": [
        {
          "id": "ap-west",
          "hourly": 0.02,
          "monthly": 20
        },
        {
          "id": "ap-northeast",
          "hourly": 0.02,
          "monthly": 20
        }
      ],
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
