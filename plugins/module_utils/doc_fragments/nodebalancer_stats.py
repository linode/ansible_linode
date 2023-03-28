"""Documentation fragments for the nodebalancer_stats module"""

specdoc_examples = ['''
- name: List all of the Nodebalancer Stats for the Nodebalancer with the given id
  linode.cloud.nodebalancer_stats:
    id: 12345''']

result_nodebalancer_stats_samples = ['''[
   {
      "connections": [
        null
       ],
       "traffic": {
        "in": [
            null
        ],
        "out": [
            null
        ]
       }
       "title" : "sample-title"
    }
]''']
