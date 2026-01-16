"""Documentation fragments for the Image Share Group Member module"""
specdoc_examples = ['''
- name: Create an image share group member
  linode.cloud.image_share_group_member:
    label: "my-sharegroup-member"
    token: "abcdefghijklmnopqrstuvwxyz1234567890"
    state: present''', '''
- name: Delete an image share group member
  linode.cloud.image_share_group_member:
    label: "my-sharegroup-member"
    state: absent''']

result_image_share_group_member_samples = ['''{
   "token_uuid": "24wef-243qg-45wgg-q343q",
   "status": "active",
   "label": "my-sharegroup-member",
   "created": "2016-03-16T17:30:49", 
   "updated": "2016-03-18T17:30:49", 
   "expiry": "2016-03-18T17:30:49"
}
''']
