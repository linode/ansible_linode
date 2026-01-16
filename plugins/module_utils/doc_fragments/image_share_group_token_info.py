"""Documentation fragments for the image_share_group_token_info module"""

specdoc_examples = ['''
- name: Get info about an Image Share Group Token by label
  linode.cloud.image_share_group_token_info:
    label: example-image-share-group-token''']

result_image_share_group_token_samples = ['''{
    "created": "2025-08-04T10:09:09",
    "expiry": "2025-08-04T10:09:11",
    "label": "example-token",
    "sharegroup_label": "example-sharegroup",
    "sharegroup_uuid": "e1d0e58b-f89f-4237-84ab-b82077342359",
    "status": "active",
    "token_uuid": "13428362-5458-4dad-b14b-8d0d4d648f8c",
    "updated": "2025-08-04T10:09:10",
    "valid_for_sharegroup_uuid": "e1d0e58b-f89f-4237-84ab-b82077342359"
}''']
