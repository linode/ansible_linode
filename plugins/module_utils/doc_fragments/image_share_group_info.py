"""Documentation fragments for the image_share_group_info module"""

specdoc_examples = ['''
- name: Get info about an Image Share Group by label
  linode.cloud.image_share_group_info:
    label: example-image-share-group''']

result_image_share_group_samples = ['''{
  "created": "2025-04-14T22:44:02",
  "description": "Example.",
  "expiry": "2025-04-14T22:44:02",
  "id": 1,
  "images_count": 0,
  "is_suspended": false,
  "label": "example-image-share-group",
  "members_count": 0,
  "updated": "2025-04-14T22:44:02",
  "uuid": "1533863e-16a4-47b5-b829-ac0f35c13278"
}''']
