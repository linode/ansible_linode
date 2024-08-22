"""Documentation fragments for the nodebalancer_stats module"""

specdoc_examples = ['''
- name: List all of the Nodebalancer Stats for the Nodebalancer with the given id
  linode.cloud.nodebalancer_stats:
    id: 12345
- name: List all of the Nodebalancer Stats for the Nodebalancer with the given label
  linode.cloud.nodebalancer_stats:
    label: example_label''']

result_nodebalancer_stats_samples = ['''[
  {
    "connections": [
      1679586600000,
      0
    ],
    "traffic": {
      "in": [
        1679586600000,
        0
      ],
      "out": [
        1679586600000,
        0
      ]
    },
    "title" : "sample-title"
  }
]''']
