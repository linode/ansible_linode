"""Documentation fragments for the vpc_info module"""

specdoc_examples = ['''
- name: Get info about a Linode type by ID
  linode.cloud.type_info:
    id: g6-standard-2''']

result_type_samples = ['''
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
}''']
