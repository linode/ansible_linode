"""Documentation fragments for the Image Share Group Token module"""
specdoc_examples = ['''
- name: Create an image share group token
  linode.cloud.image_share_group_token:
    label: "my-sharegroup-token"
    valid_for_sharegroup_uuid: "1533863e-16a4-47b5-b829-ac0f35c13278"
    state: present''', '''
- name: Delete an image share group
  linode.cloud.image_share_group_token:
    valid_for_sharegroup_uuid: "e1d0e58b-f89f-4237-84ab-b82077342359"
    state: absent''']

result_image_share_group_token_samples = ['''{
  "created": "2025-08-04T10:09:09",
  "expiry": null,
  "label": "Backend Services - Engineering",
  "sharegroup_label": "DevOps Base Images",
  "sharegroup_uuid": "e1d0e58b-f89f-4237-84ab-b82077342359",
  "status": "active",
  "token_uuid": "13428362-5458-4dad-b14b-8d0d4d648f8c",
  "updated": null,
  "valid_for_sharegroup_uuid": "e1d0e58b-f89f-4237-84ab-b82077342359"
}''']

result_single_use_token_samples = ['''{
  "token": "abcdefghijklmnopqrstuvwxyz1234567890"
}''']