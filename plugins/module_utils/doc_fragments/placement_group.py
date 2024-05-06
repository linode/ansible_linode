"""Documentation fragments for the placement_group module"""

specdoc_examples = ['''
- name: Create a placement group
  linode.cloud.placement_group:
    label: my-pg
    region: us-east
    affinity_type: anti_affinity:local
    is_strict: True
    state: present''', '''
- name: Update a placement group label
  linode.cloud.placement_group:
    label: my-pg-updated
    region: us-east
    affinity_type: anti_affinity:local
    is_strict: True
    state: present''', '''
- name: Delete a placement group
  linode.cloud.placement_group:
    label: my-pg
    state: absent''']

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
