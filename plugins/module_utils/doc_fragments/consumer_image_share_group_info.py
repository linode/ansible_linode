"""Documentation fragments for the image_share_group_info module"""

specdoc_examples = ['''
- name: Get info about an Image Share Group by a Consumer's Token UUID
  linode.cloud.consumer_image_share_group_info:
    token_uuid: "1433863e-16a4-47b5-b829-ac0f35c13278"''']

result_consumer_image_share_group_samples = ['''{
  "created": "2025-04-14T22:44:02",
  "description": "Group of base operating system images and engineers used for CI/CD pipelines and infrastructure automation",
  "id": 1,
  "is_suspended": false,
  "label": "DevOps Base Images",
  "updated": "2025-04-14T22:44:03",
  "uuid": "1533863e-16a4-47b5-b829-ac0f35c13278"
}''']
