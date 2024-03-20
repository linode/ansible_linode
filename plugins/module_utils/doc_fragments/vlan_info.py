"""Documentation fragments for the vlan_info module"""

specdoc_examples = ['''
- name: Get info about a VLAN by label
  linode.cloud.vlan_info:
    api_version: v4beta
    label: example-vlan''']

result_vlan_samples = ['''{
  "created": "2020-01-01T00:01:01",
  "label": "vlan-example",
  "linodes": [
    111,
    222
  ],
  "region": "ap-west"
}''']
