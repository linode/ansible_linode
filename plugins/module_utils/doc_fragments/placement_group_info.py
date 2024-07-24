"""Documentation fragments for the placement_group module"""

result_placement_group_samples = ['''
{
  "id": 123,
  "label": "test",
  "region": "eu-west",
  "placement_group_type": "anti_affinity:local",
  "placement_group_policy": "strict",
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
