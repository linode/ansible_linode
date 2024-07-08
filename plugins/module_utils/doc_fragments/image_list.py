"""Documentation fragments for the image_info module"""

specdoc_examples = ['''
- name: List all of the images for the current Linode Account
  linode.cloud.image_list: {}''', '''
- name: List the latest 5 images for the current Linode Account
  linode.cloud.image_list:
    count: 5
    order_by: created
    order: desc''', '''
- name: Resolve all Alpine Linux images
  linode.cloud.image_list:
    filters:
      - name: vendor
        values: Alpine''']

result_images_samples = ['''[
   {
      "created":"2021-08-14T22:44:02",
      "created_by":"my-account",
      "deprecated":false,
      "description":"Example Image description.",
      "eol":"2026-07-01T04:00:00",
      "expiry":null,
      "id":"private/123",
      "is_public":false,
      "label":"test",
      "size":2500,
      "status":null,
      "type":"manual",
      "updated":"2021-08-14T22:44:02",
      "vendor":"Debian",
      "tags": ["test"],
      "total_size": 5000,
      "regions": [
        {
            "region": "us-east",
            "status": "available"
        },
        {
            "region": "us-central",
            "status": "pending"
        }]
       }
]''']
