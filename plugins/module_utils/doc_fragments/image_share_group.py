"""Documentation fragments for the Image Share Group module"""
specdoc_examples = ['''
- name: Create a basic image share group
  linode.cloud.image_share_group:
    label: "my-sharegroup"
    description: "My image share group."
    state: present''', '''
- name: Create a basic image share group with an image
  linode.cloud.image_share_group:
    label: "my-sharegroup"
    description: "My image share group."
    images:
      - id: "private/123"
        label: "My shared image"
        description: "An image shared in the group."
    state: present
    ''', '''
- name: Delete an image share group
  linode.cloud.image_share_group:
    label: "my-sharegroup"
    state: absent''']

result_image_share_group_samples = ['''{
  "created": "2025-04-14T22:44:02",
  "description": "My image share group.",
  "expiry": null,
  "id": 1,
  "images_count": 0,
  "is_suspended": false,
  "label": "my-sharegroup",
  "members_count": 0,
  "updated": null,
  "uuid": "1533863e-16a4-47b5-b829-ac0f35c13278"
}''']
