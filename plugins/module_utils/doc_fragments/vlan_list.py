"""Documentation fragments for the vlan_list module"""

specdoc_examples = ['''
- name: List all of the VLANs for the current Linode Account
  linode.cloud.vlan_list:
    api_version: v4beta''', '''
- name: List all VLANs in the us-southeast region
  linode.cloud.vlan_list:
    api_version: v4beta
    filters:
      - name: region
        values: us-southeast
''']

result_vlan_samples = ['''[
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
