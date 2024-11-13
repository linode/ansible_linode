"""Documentation fragments for the network_transfer_prices_list module"""

specdoc_examples = ['''
- name: List all of the Linode Network Transfer Prices
  linode.cloud.network_transfer_prices_list: {}''', '''
- name: List a Linode Network Transfer Price named Distributed Network Transfer
  linode.cloud.network_transfer_prices_list:
    filters:
      - name: label
        values: Distributed Network Transfer
''']

result_network_transfer_prices_samples = ['''[
    {
        "id": "distributed_network_transfer",
        "label": "Distributed Network Transfer",
        "price": {
            "hourly": 0.01,
            "monthly": null
        },
        "region_prices": [],
        "transfer": 0
    }
]''']
