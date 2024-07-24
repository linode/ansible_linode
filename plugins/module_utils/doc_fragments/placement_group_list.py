"""Documentation fragments for the placement_group_list module"""

specdoc_examples = ['''
- name: List all of Linode placement group for the current account
  linode.cloud.placement_group_list:
    api_version: v4beta''']

result_placement_groups_samples = ['''[
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
]''']
