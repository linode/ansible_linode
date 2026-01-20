"""Documentation fragments for the image_share_group_member_list module"""

specdoc_examples = ['''
- name: List all of the Image Share Group Members for the specified Share Group
  linode.cloud.image_share_group_member_list: 
    sharegroup_id: 123''']

result_image_share_group_members_samples = ['''[
    {
      "created": "2025-08-04T10:07:59",
      "expiry": "2025-08-04T10:08:01",
      "label": "member-label",
      "status": "active",
      "token_uuid": "4591075e-4ba8-43c9-a521-928c3d4a135d",
      "updated": "2025-08-04T10:08:00"
    }
]''']
