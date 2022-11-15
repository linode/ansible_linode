"""Documentation fragments for the vlans_list module"""

specdoc_examples = ['''
- name: List all of the VLANs for the current Linode Account
  linode.cloud.vlans_list: {}''', '''
- name: List the latest 5 VLANs for the current Linode Account
  linode.cloud.vlans_list:
    count: 5
    order_by: desc
    order: created''']

result_vlans_samples = ['''[
   {
   "created": "2020-01-01T00:01:01",
    "label": "vlan-example",
    "linodes": [
        111,
        222
      ],
      "region": "ap-west"
   }
]''']
