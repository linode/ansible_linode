"""Documentation fragments for the placement_group_assign module"""

specdoc_examples = ['''
- name: Assign a Linode to a placement group
  linode.cloud.placement_group_assign:
    placement_group_id: 123
    linode_id: 111
    state: present''', '''
- name: Unassign a Linode from a placement group
  linode.cloud.placement_group_assign:
    placement_group_id: 123
    linode_id: 111
    state: absent
''']
