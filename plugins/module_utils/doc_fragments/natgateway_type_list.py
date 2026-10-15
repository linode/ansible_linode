"""Documentation fragments for the nat_gateway_type_list module"""

specdoc_examples = ['''
- name: List all of the NAT Gatewat Types
  linode.cloud.natgateway_type_list: {}''', '''
''']

result_natgateway_type_samples = ['''[
    {
      "id": "g1-natgateway",
      "label": "NAT Gateway",
      "price": {
        "hourly": 0.035
      },
      "region_prices": [],
      "transfer": 0
    }
]''']
