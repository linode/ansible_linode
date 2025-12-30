"""Documentation fragments for the image_share_group_list module"""

specdoc_examples = ['''
- name: List all of the Image Share Groups for the current Linode Account
  linode.cloud.image_share_group_list: {}''']

result_image_share_groups_samples = ['''[
    {
      "created": "2025-04-14T22:44:02",
      "description": "Group of base operating system images and engineers used for CI/CD pipelines and infrastructure automation",
      "expiry": null,
      "id": 1,
      "images_count": 0,
      "is_suspended": false,
      "label": "DevOps Base Images",
      "members_count": 0,
      "updated": null,
      "uuid": "1533863e-16a4-47b5-b829-ac0f35c13278"
    }
]''']
