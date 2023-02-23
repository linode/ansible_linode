"""Documentation fragments for the region_list module"""

specdoc_examples = ['''
- name: List all of the Linode regions
  linode.cloud.region_list: {}''', '''
- name: Resolve all Linode regions
  linode.cloud.region_list:
    filter:
      - name: id
        values: us-east''']

result_images_samples = ['''[
   {
      "capabilities": [
        "Linodes",
        "NodeBalancers",
        "Block Storage",
        "Object Storage"
      ],
      "country": "us",
      "id": "us-east",
      "label": "Newark, NJ, USA",
      "resolvers": {
        "ipv4": "192.0.2.0,192.0.2.1",
        "ipv6": "2001:0db8::,2001:0db8::1"
      },
      "status": "ok"
    }
]''']
