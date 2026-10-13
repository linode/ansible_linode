"""Documentation fragments for the natgateway_interface_address_list module"""

specdoc_examples = ['''
- name: List the Interfaces for a NAT Gateway that are using the specified IP Address
  linode.cloud.natgateway_address_interface_list:
    id: 123
    address: 203.0.113.43''']

result_natgateway_address_interface_samples = ['''[
    {
      "id": 142,
      "linode": {
        "id": 1001,
        "label": "linode1001",
        "type": "linode",
        "url": "/v4/linode/instances/1001"
      }
    },
    {
      "id": 143,
      "linode": {
        "id": 1002,
        "label": "linode1002",
        "type": "linode",
        "url": "/v4/linode/instances/1002"
      }
  ]''']
