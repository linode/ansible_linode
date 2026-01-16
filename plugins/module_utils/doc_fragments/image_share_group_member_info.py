"""Documentation fragments for the image_share_group_member_info module"""

specdoc_examples = ['''
- name: Get info about an Image Share Group Member by label
  linode.cloud.image_share_group_member_info:
    sharegroup_id: 123456
    label: example-image-share-group-member''']

result_image_share_group_member_samples = ['''{
  "created": "2025-08-04T10:07:59",
  "expiry": "2025-08-04T10:08:01",
  "label": "Engineering - Backend",
  "status": "active",
  "token_uuid": "4591075e-4ba8-43c9-a521-928c3d4a135d",
  "updated": "2025-08-04T10:08:00"
}''']
