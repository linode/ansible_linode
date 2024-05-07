"""Documentation fragments for the placement_group module"""

specdoc_examples = ['''
- name: Create a placement group
  linode.cloud.placement_group:
    label: my-pg
    region: us-east
    affinity_type: anti_affinity:local
    is_strict: True
    state: present''', '''
- name: Update a Linode placement group label
  linode.cloud.placement_group:
    # id is required to update the label
    id: 123
    label: my-pg-updated
    state: present''', '''
- name: Delete a placement group by label
  linode.cloud.placement_group:
    label: my-pg
    state: absent''', '''
- name: Delete a placement group by id
  linode.cloud.placement_group:
    id: 123
    state: absent    
''']

result_placement_group_samples = ['''{
  "id": 123,
  "label": "my-pg",
  "region": "eu-west",
  "affinity_type": "anti_affinity:local",
  "is_strict": true,
  "is_compliant": true,
  "members": [
    {
      "linode_id": 123,
      "is_compliant": true
    }
  ]
}''']
