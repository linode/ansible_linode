"""Documentation fragments for the natgateway_interface_list module"""

specdoc_examples = ['''
- name: List the Interfaces for a NAT Gateway
  linode.cloud.natgateway_interface_list:
    id: 123''']

result_natgateway_interface_samples = ['''[
    {
      "addresses": [
        "203.0.113.42",
        "203.0.113.43"
      ],
      "id": 142,
      "linode": {
        "id": 1001,
        "label": "linode1001",
        "type": "linode",
        "url": "/v4/linode/instances/1001"
      }
    },
    {
      "addresses": [
        "203.0.113.42",
        "203.0.113.43"
      ],
      "id": 143,
      "linode": {
        "id": 1002,
        "label": "linode1002",
        "type": "linode",
        "url": "/v4/linode/instances/1002"
      }
    }
  ]''']
