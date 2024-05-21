"""Documentation fragments for the placement_group module"""

result_placement_group_samples = ['''
{
  "id": 123,
  "label": "test",
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
}
''']


specdoc_examples = ['''
- name: Get info about a Linode placement group
  linode.cloud.placement_group_info: 
    api_version: v4beta
    id: 123
''']
