"""Documentation fragments for the image_share_group_token_list module"""

specdoc_examples = ['''
- name: List all of the Image Share Group Tokens for the current Linode Account
  linode.cloud.image_share_group_token_list: {}''']

result_image_share_group_tokens_samples = ['''[
    {
      "created": "2025-08-04T10:09:09",
      "expiry": "2025-08-04T10:09:11",
      "label": "example-token",
      "sharegroup_label": "example-sharegroup",
      "sharegroup_uuid": "e1d0e58b-f89f-4237-84ab-b82077342359",
      "status": "active",
      "token_uuid": "13428362-5458-4dad-b14b-8d0d4d648f8c",
      "updated": "2025-08-04T10:09:10",
      "valid_for_sharegroup_uuid": "e1d0e58b-f89f-4237-84ab-b82077342359"
    }
]''']
